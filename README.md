#Merge Bot 3000

##Status

This is what I would consider to be pre-release and not yet ready to do anything. It has the basic functionality of being able to call github to see what needs to be merged and do the actual merge upon command. However, it is severly lacking in tests and error handling.

##Usage

The basic idea of this is for automatic merges on a scheduled basis. While not useful everywhere, it could be incredibly useful for scheduled builds or merging new blog posts automatically. You would give the bot collaborator status on a repo and tell it to merge by mentioning it in the pull request. For example ``@mergebot3000 merge at 12/25/2013 at 05:00`` would translate into an automatic merge at December 25, 2013, 5 a.m. UTC.

##Commands

``python manage.py get_new_requests`` will get all new requests from the notification api on github and put them in the database.

``python manage.py merge_upcoming_requests`` will merge all requests scheduled for the next ten minutes.

##TODO

1. Better testing.
2. Set up the admin panel.
3. Options as to who has the power to issue a merge request.
4. Better error handling and logging.
5. Home page listing what is upcoming and server time.
