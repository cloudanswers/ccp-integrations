ccp-integrations
================

Our internal integrations for our business systems.  The following business processes are implemented:

1.  Create Toggl Project when PivotalTracker Story is started so we can log our time on the task


Dev Setup
---------

    $ git clone <repo>
    $ virtualenv venv
    $ . ./venv/bin/activate
    $ pip install -r requirements.txt
    $ #### start the dev web server
    $ python app.py


Todo
----

1. Add process for Freshbooks Project to PivotalTracker Epic
1. Add process for Freshbooks Project to Salesforce (maybe optional since already sync'd via appx package)
1. Add process for Freshbooks Project to Hipchat notification
1. Add process for Odesk * to Salesforce *
1. Add process for Toggl Time Entries to Freshbooks Time Entries
1. Update process for PivotalTracker Story to Toggl Project to be more selective about when it runs the sync, currently every time anything is edited


License
-------

Affero GPL