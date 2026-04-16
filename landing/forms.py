from django import forms
from django.core.mail import EmailMessage
from django.conf import settings

from .models import Lead


class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ['name', 'company', 'email', 'phone', 'need']
        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'field__input', 'placeholder': 'Tu nombre'}
            ),
            'company': forms.TextInput(
                attrs={'class': 'field__input', 'placeholder': 'Nombre de tu empresa'}
            ),
            'email': forms.EmailInput(
                attrs={'class': 'field__input', 'placeholder': 'correo@empresa.com'}
            ),
            'phone': forms.TextInput(
                attrs={'class': 'field__input', 'placeholder': 'Telefono o WhatsApp'}
            ),
            'need': forms.Textarea(
                attrs={
                    'class': 'field__input field__input--textarea',
                    'placeholder': 'Cuentanos que proceso quieres digitalizar o acelerar.',
                    'rows': 5,
                }
            ),
        }
        labels = {
            'need': 'Necesidad',
        }

    def save(self, commit=True):
        """
        Sobrescribe el método save para enviar automáticamente un correo cuando
        se completa el formulario.
        """
        lead = super().save(commit=commit)
        if commit:
            self.send_notification_email(lead)
        return lead

    def send_notification_email(self, lead):
        """
        Envía un correo de notificación con la información del Lead.
        
        CONFIGURACIÓN IMPORTANTE:
        La dirección de correo where_to_receive_emails debe ser configurada en settings.py
        Ejemplo en settings.py:
            CONTACT_EMAIL = 'tu-email@ejemplo.com'  # Aquí es donde recibirás los correos
        """
        try:
            # LUGAR DONDE CONFIGURAR EL CORREO DE DESTINO:
            # En settings.py, agrega esta línea:
            # CONTACT_EMAIL = 'tu-email-destino@empresa.com'
            recipient_email = getattr(settings, 'CONTACT_EMAIL', None)
            
            if not recipient_email:
                print("⚠️ ADVERTENCIA: CONTACT_EMAIL no está configurado en settings.py")
                print("El correo NO fue enviado. Configura CONTACT_EMAIL en settings.py")
                return
            
            # Asunto: Nombre + Empresa
            subject = f"{lead.name} - {lead.company}"
            
            # Cuerpo del correo:
            # Primero: Contenido del campo de necesidad
            # Correo del usuario y teléfono
            message = f"""{lead.need}

---
De: {lead.name}
Correo: {lead.email}
Empresa: {lead.company}
Otra forma de contacto: {lead.phone}
            """
            
            # Remitente (from): Usa la configurada en settings.py (DEFAULT_FROM_EMAIL)
            # El email del usuario se coloca en reply_to para que las respuestas vayan a él
            from_email = settings.DEFAULT_FROM_EMAIL
            
            # Enviar correo usando EmailMessage (soporta reply_to)
            email = EmailMessage(
                subject=subject,
                body=message,
                from_email=from_email,
                to=[recipient_email],
                reply_to=[lead.email],  # Las respuestas van al email del usuario
            )
            email.send(fail_silently=False)
            print(f"✅ Correo enviado exitosamente a {recipient_email}")
            print(f"📧 Responder a: {lead.email}")
        except Exception as e:
            print(f"❌ Error al enviar el correo: {str(e)}")