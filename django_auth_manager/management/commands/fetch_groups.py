import sys
import yaml
from itertools import zip_longest

from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand

from django_auth_manager.constants import DEFAULT_LENGTH


class Command(BaseCommand):
    help = "List all groups, users in them and the permissions in these groups"

    def add_arguments(self, parser):
        parser.add_argument(
            "-g",
            "--group",
            dest="group_name",
            required=False,
            help="Specify group name to retrieve information for a specific group",
        )
        parser.add_argument(
            "--yaml",
            action="store_true",
            default=False,
            help="Output the data in yaml format",
        )
        parser.add_argument(
            "--table",
            action="store_true",
            default=False,
            help="Output the data as a table",
        )

    def handle(self, *args, **options):
        groups_data = self._get_groups_list(options["group_name"])
        if options["yaml"]:
            self.stdout.write(yaml.dump(groups_data))
        elif options["table"]:
            self._output_groups_users_permissions_table(groups_data)
        else:
            self.stderr.write(
                self.style.ERROR(
                    "Specify in which format you want to output the data."
                    " Use --help to get the available options"
                )
            )
            sys.exit(1)

    def _get_groups_list(self, group_name):
        """
        Return a list of dicts that represent groups. Each dict contains of a group name,
        permissions for this group, and users in it
        """
        if group_name:
            all_groups = Group.objects.prefetch_related(
                "user_set", "permissions"
            ).filter(name=group_name)
            if not all_groups.exists():
                self.stderr.write(self.style.ERROR(f"Group {group_name} is not found"))
                sys.exit(1)
        else:
            all_groups = Group.objects.prefetch_related("user_set", "permissions").all()

        groups_data = []
        for group in all_groups:
            # Prepare data dictionary for each group
            group_data = {
                "name": group.name,
                "permissions": [],
                "users": [],
            }

            # Add users to the group data
            for user in group.user_set.all():
                if user.email:
                    group_data["users"].append(f"{user.username} ({user.email})")
                else:
                    group_data["users"].append(f"{user.username}")

            # Add permissions to the group data
            for permission in group.permissions.all():
                group_data["permissions"].append(permission.codename)

            # Add the group's data to the list
            groups_data.append(group_data)
        return groups_data

    def _output_groups_users_permissions_table(self, groups_data):
        max_group_name_length = (
            max(len(group["name"]) for group in groups_data)
            if groups_data
            else DEFAULT_LENGTH
        )
        max_user_length = (
            max(
                (max(len(user) for user in group["users"]) if group["users"] else 0)
                for group in groups_data
            )
            if groups_data
            else DEFAULT_LENGTH
        )
        max_permission_length = (
            max(
                (
                    max(len(perm) for perm in group["permissions"])
                    if group["permissions"]
                    else 0
                )
                for group in groups_data
            )
            if groups_data
            else DEFAULT_LENGTH
        )

        # Total width for the delimiter line
        total_width = (
            max_group_name_length + max_user_length + max_permission_length + 6
        )  # 6 for pipes and spaces

        # Print header with dynamic spacing
        self.stdout.write(
            f"{'Group':<{max_group_name_length}} | {'User':<{max_user_length}} | {'Permission':<{max_permission_length}}"
        )
        self.stdout.write("-" * total_width)

        # Iterate through each group
        for group in groups_data:
            self.stdout.write(f"{group['name']:<{max_group_name_length}} | ", ending="")
            if group["users"]:
                self.stdout.write(
                    f"{group['users'][0]:<{max_user_length}} | ", ending=""
                )
            else:
                self.stdout.write(f"{'No users':<{max_user_length}} | ", ending="")
            if group["permissions"]:
                self.stdout.write(f"{group['permissions'][0]:<{max_permission_length}}")
            else:
                self.stdout.write(f"{'No permissions':<{max_permission_length}}")

            users_perms = list(
                zip_longest(group["users"][1:], group["permissions"][1:], fillvalue="")
            )

            for user, perm in users_perms:
                self.stdout.write(
                    f"{' ':<{max_group_name_length}} | {user:<{max_user_length}} | {perm:<{max_permission_length}}"
                )

            # Print delimiter line after each group's data
            self.stdout.write("-" * total_width)
