pivotaltracker-toggl-integration
================================

Sync active PivotalTracker stories to Toggl so we can log our time.  It runs on heroku with an hourly scheduled job and a webhook from PivotalTracker that will execute the sync any time a change in PivotalTracker happens.

Todo
----

1. Link Toggl Projects to Clients based on PivotalTracker Tag that matches 
1. Make it be more selective about when it runs the sync (not when just editing something in the icebox)
