import os
import subprocess
import logging
from celery import shared_task
from django.conf import settings

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3)
def compress_video(self, video_id: int):
    """
    Compresse une vidéo uploadée en H.264 (MP4) via ffmpeg.

    Paramètres ffmpeg utilisés :
      -vcodec libx264  → codec vidéo H.264 (meilleur support universel)
      -crf 23          → qualité constante (0=lossless, 51=pire ; 23 = bon équilibre)
      -preset medium   → vitesse de compression vs taille du fichier
      -acodec aac      → codec audio AAC (standard streaming)
      -movflags +faststart → déplace les métadonnées en début de fichier pour
                             permettre la lecture streaming avant téléchargement complet
    """
    # Import ici pour éviter les imports circulaires
    from film.models import Video

    try:
        video = Video.objects.get(pk=video_id)
    except Video.DoesNotExist:
        logger.error(f"compress_video: Video id={video_id} introuvable.")
        return

    # Marquer comme "en cours"
    video.compression_status = 'processing'
    video.save(update_fields=['compression_status'])

    input_path = video.file.path
    if not os.path.exists(input_path):
        logger.error(f"compress_video: Fichier source introuvable : {input_path}")
        video.compression_status = 'error'
        video.save(update_fields=['compression_status'])
        return

    # Construire le chemin du fichier de sortie compressé
    base, ext = os.path.splitext(input_path)
    output_path = base + '_compressed.mp4'

    cmd = [
        'ffmpeg',
        '-i', input_path,
        '-vcodec', 'libx264',
        '-crf', '23',
        '-preset', 'medium',
        '-acodec', 'aac',
        '-movflags', '+faststart',
        '-y',           # Écraser si le fichier existe déjà
        output_path,
    ]

    logger.info(f"compress_video: Démarrage compression id={video_id} : {input_path}")

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=3600,  # Timeout 1h max
        )
    except subprocess.TimeoutExpired:
        logger.error(f"compress_video: Timeout pour id={video_id}")
        video.compression_status = 'error'
        video.save(update_fields=['compression_status'])
        return
    except FileNotFoundError:
        logger.error("compress_video: ffmpeg n'est pas installé ou introuvable dans le PATH.")
        video.compression_status = 'error'
        video.save(update_fields=['compression_status'])
        return

    if result.returncode == 0 and os.path.exists(output_path):
        # Supprimer l'original et pointer vers le fichier compressé
        try:
            os.remove(input_path)
        except OSError as e:
            logger.warning(f"compress_video: Impossible de supprimer l'original : {e}")

        # Mettre à jour le chemin relatif stocké en DB
        relative_output = os.path.relpath(output_path, settings.MEDIA_ROOT).replace('\\', '/')
        video.file.name = relative_output
        video.compression_status = 'done'
        video.save(update_fields=['file', 'compression_status'])

        original_size = "N/A"
        compressed_size = os.path.getsize(output_path) / (1024 * 1024)
        logger.info(f"compress_video: Terminé id={video_id}. Taille finale : {compressed_size:.1f} MB")
    else:
        logger.error(f"compress_video: Échec ffmpeg (code {result.returncode}) :\n{result.stderr}")
        video.compression_status = 'error'
        video.save(update_fields=['compression_status'])

        # Réessayer automatiquement si ffmpeg retourne une erreur récupérable
        raise self.retry(exc=Exception(result.stderr), countdown=60)
