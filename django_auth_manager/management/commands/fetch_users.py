import sys
from django.contrib.auth.models import User, Permission
from django.core.management.base import BaseCommand

from django_auth_manager.constants import INDENT


class Command(BaseCommand):
    help = "List all users and their permissions, including those inherited from groups."

    def add_arguments(self, parser):
        parser.add_argument(
            "-u",
            "--user",
            dest="username",
            required=False,
            help="Specify username to retrieve information for a specific user",
        )

    def handle(self, *args, **options):
        if options["username"]:
            users = User.objects.filter(username=options["username"])
            if not users.exists():
                self.stderr.write(
                    self.style.ERROR(f"User {options['username']} is not found")
                )
                sys.exit(1)
        else:
            users = User.objects.all()

        for user in users:
            # Permissions assigned directly to a users
            direct_permissions = user.user_permissions.all()
            # Permissions inherited by a user from their groups
            group_permissions = user.groups.values_list("permissions", flat=True)

            permissions = set(direct_permissions) | set(group_permissions)

            if user.email:
                self.stdout.write(
                    self.style.SUCCESS(f"User: {user.username} ({user.email})")
                )
            else:
                self.stdout.write(self.style.SUCCESS(f"User: {user.username}"))
            if user.is_superuser:
                self.stdout.write(self.style.WARNING(f"{INDENT}This is a superuser."))
                self.stdout.write(
                    self.style.WARNING(
                        f"{INDENT}The permissions below will be kept with a user even if"
                        " you remove the superuser bit from their account."
                    )
                )
            if permissions:
                self.stdout.write(f"{INDENT}Permissions:")
                for perm in permissions:
                    try:
                        self.stdout.write(
                            f"{INDENT}- {Permission.objects.get(pk=perm).codename}"
                        )
                    except TypeError:
                        self.stdout.write(f"{INDENT}- {perm.codename}")
                    except Permission.DoesNotExist:
                        continue
            else:
                self.stdout.write(f"{INDENT}No permissions found.")
