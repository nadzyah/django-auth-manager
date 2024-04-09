# Django Auth Manager

This is a Django extension that extends `manage.py` commands and provides the ability to retrieve information about users, groups and their permissions.

## Installation

Install using PIP:

```bash
pip install django-auth-manager
```

Add django\_auth\_manager to INSTALLED\_APPS:

```
INSTALLED_APPS += ["django_auth_manager"]
```

## Usage

This extension provides you with additional `manage.py` commands. The information below describes how to use them.

## Fetch All Users and Their Permissions

The `fetch_users` script outputs the information about a user and their permissions. Here is an example for getting information for all the users:

```bash
$ ./manage.py fetch_users
User: nadzeya (nadzya.info@gmail.com)
  This is a superuser.
  The permissions below will be kept with a user even if you remove the superuser bit from their account.
  No permissions found.
User: testuser
  Permissions:
  - view_userexperience
  - add_topic
  - change_topic
  - delete_topic
  - view_topic
  - add_task
  - change_task
  - delete_task
  - view_task
  - view_userwordprogress
  - add_word
  - change_word
  - delete_word
  - view_word
  - view_usertaskprogress
  - add_userexperience
  - change_userexperience
  - delete_userexperience
```

You can also specify a username to get information for a specific user:

```bash
./manage.py fetch_users -u testuser
User: testuser
  Permissions:
  - view_userexperience
  - add_topic
  - change_topic
  - delete_topic
  - view_topic
  - add_task
  - change_task
  - delete_task
  - view_task
  - view_userwordprogress
  - add_word
  - change_word
  - delete_word
  - view_word
  - view_usertaskprogress
  - add_userexperience
  - change_userexperience
  - delete_userexperience
```


## Fetch Information About Groups

The `fetch_groups` command outputs all the groups, users in these groups, and the group permissions for each group. You can output the data in either YAML or table format:

```bash
$ ./manage.py fetch_groups --yaml
- name: Developers
  permissions:
  - view_user
  - view_token
  - view_emailverificationcode
  - view_passwordresettoken
  - view_task
  - change_topic
  - view_topic
  - view_userexperience
  - view_usertaskprogress
  - view_userwordprogress
  - view_word
  users: []
- name: Administrators
  permissions:
  - add_task
  - change_task
  - delete_task
  - view_task
  - add_topic
  - change_topic
  - delete_topic
  - view_topic
  - add_userexperience
  - change_userexperience
  - delete_userexperience
  - view_userexperience
  - view_usertaskprogress
  - view_userwordprogress
  - add_word
  - change_word
  - delete_word
  - view_word
  users:
  - testuser
```

Here you can see how the table format looks:

```bash
$ ./manage.py fetch_groups --table
Group          | User     | Permission                
------------------------------------------------------
Developers     | No users | view_user                 
               |          | view_token                
               |          | view_emailverificationcode
               |          | view_passwordresettoken   
               |          | view_task                 
               |          | change_topic              
               |          | view_topic                
               |          | view_userexperience       
               |          | view_usertaskprogress     
               |          | view_userwordprogress     
               |          | view_word                 
------------------------------------------------------
Administrators | testuser | add_task                  
               |          | change_task               
               |          | delete_task               
               |          | view_task                 
               |          | add_topic                 
               |          | change_topic              
               |          | delete_topic              
               |          | view_topic                
               |          | add_userexperience        
               |          | change_userexperience     
               |          | delete_userexperience     
               |          | view_userexperience       
               |          | view_usertaskprogress     
               |          | view_userwordprogress     
               |          | add_word                  
               |          | change_word               
               |          | delete_word               
               |          | view_word                 
------------------------------------------------------
```

By specifying `-g $GROUP_NAME`, you can fetch the information about a specific group:

```bash
$ ./manage.py fetch_groups --table -g Administrators
Group          | User     | Permission           
-------------------------------------------------
Administrators | testuser | add_task             
               |          | change_task          
               |          | delete_task          
               |          | view_task            
               |          | add_topic            
               |          | change_topic         
               |          | delete_topic         
               |          | view_topic           
               |          | add_userexperience   
               |          | change_userexperience
               |          | delete_userexperience
               |          | view_userexperience  
               |          | view_usertaskprogress
               |          | view_userwordprogress
               |          | add_word             
               |          | change_word          
               |          | delete_word          
               |          | view_word            
-------------------------------------------------
```
