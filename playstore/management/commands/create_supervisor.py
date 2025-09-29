# playstore/management/commands/create_supervisor.py
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.db import transaction
from typing import Optional

from playstore.models import UserProfile  # ensure this model exists

class Command(BaseCommand):
    help = "Create or update a user and grant/revoke supervisor capability."

    def add_arguments(self, parser):
        parser.add_argument("username", type=str, help="Username to create or update")
        parser.add_argument("--password", type=str, default=None, help="Password for the user (optional)")
        parser.add_argument("--email", type=str, default=None, help="Email for the user (optional)")
        parser.add_argument("--remove", action="store_true", help="Revoke supervisor role instead of granting")
        parser.add_argument("--no-input", action="store_true", help="Do not prompt for password; error if missing")

    @transaction.atomic
    def handle(self, *args, **options):
        username: str = options["username"]
        password: Optional[str] = options.get("password")
        email: Optional[str] = options.get("email")
        remove: bool = options.get("remove", False)
        no_input: bool = options.get("no_input", False)

        # Fetch or create user
        user, created = User.objects.get_or_create(username=username, defaults={"email": email or ""})
        if not created:
            # Update email if provided
            if email is not None and user.email != email:
                user.email = email

        # Password handling
        if password:
            user.set_password(password)
        else:
            if created:
                if no_input:
                    raise CommandError(
                        "User created but no password provided and --no-input set. "
                        "Re-run with --password or without --no-input."
                    )
                # If interactive, Django will prompt later via createsuperuser semantics — but since we’re here,
                # set an unusable password so the account exists without login until set/reset.
                user.set_unusable_password()

        user.save()

        # Ensure profile exists
        profile, _ = UserProfile.objects.get_or_create(user=user)

        # Toggle supervisor
        if remove:
            if profile.is_supervisor:
                profile.is_supervisor = False
                profile.save()
                self.stdout.write(self.style.SUCCESS(f"Revoked supervisor from '{username}'."))
            else:
                self.stdout.write(self.style.WARNING(f"'{username}' is not a supervisor; nothing to revoke."))
        else:
            if not profile.is_supervisor:
                profile.is_supervisor = True
                profile.save()
                self.stdout.write(self.style.SUCCESS(f"Granted supervisor to '{username}'."))
            else:
                self.stdout.write(self.style.NOTICE(f"'{username}' is already a supervisor."))

        # Final summary
        state = "supervisor" if profile.is_supervisor else "regular user"
        self.stdout.write(self.style.SUCCESS(f"User '{username}' saved ({state})."))
