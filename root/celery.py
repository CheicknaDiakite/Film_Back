import os
from celery import Celery

# Définit le module settings Django par défaut pour celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'root.settings')

app = Celery('root')

# Charge la config Celery depuis les settings Django (préfixe CELERY_)
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-découverte des fichiers tasks.py dans toutes les apps installées
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
