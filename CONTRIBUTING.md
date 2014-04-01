Contribute to the Telerik AppBuilder Package for Sublime Text
===

*Help us improve the Telerik AppBuilder Package for Sublime Text* 

[![Telerik AppBuilder](https://raw.githubusercontent.com/Icenium/appbuilder-sublime-package/master/ab-logo.png "Telerik AppBuilder")](http://www.telerik.com/appbuilder "The Telerik AppBuilder web site")

The Telerik AppBuilder package for Sublime Text 2 lets you run your hybrid mobile app on connected devices or in the device simulator, and synchronize your code changes to the running app without redeploying it. The package requires that the Telerik AppBuilder Command-Line Interface is installed on your system.

> The Telerik AppBuilder Command-Line Interface is delivered for Windows and OS X as an npm package. For more information click <a href="https://www.npmjs.org/package/appbuilder" target="_blank">here</a>.

* [Report an Issue](#report-an-issue "Learn how to report a bug")
* [Request a Feature](#request-a-feature "Learn how to submit a feature or improvement request")
* [Contribute to the Code Base](#contribute-to-the-code-base "Learn how to submit your own improvements to the code")

Report an Issue
===
If you find a bug in the source code or a mistake in the documentation, you can help us by submitting an issue to our <a href="https://github.com/Icenium/appbuilder-sublime-package">GitHub Repository</a>.
Before you submit your issue search the archive, maybe your question was already answered.
If your issue appears to be a bug, and hasn't been reported, open a new issue. Help us to maximize the effort we can spend fixing issues and adding new features, by not reporting duplicate issues. Providing the following information will increase the chances of your issue being dealt with quickly:

* Overview of the issue - if an error is being thrown a stack trace helps
* Motivation for or Use Case - explain why this is a bug for you
* Telerik AppBuilder Version(s) - is it a regression?
* Operating System - is this a problem with all operating systems?
* Reproduce the error - provide an unambiguous set of steps.
* Related issues - has a similar issue been reported before?
* Suggest a Fix - if you can't fix the bug yourself, perhaps you can point to what might be causing the problem (line of code or commit)

[Back to Top][1]

Request a Feature
===
You can request a new feature by submitting an issue with an *enhancement* label to our <a href="https://github.com/Icenium/appbuilder-sublime-package">GitHub Repository</a>.
If you would like to implement a new feature then consider submitting it to the <a href="https://github.com/Icenium/appbuilder-sublime-package">GitHub Repository</a> as a Pull Request.

[Back to Top][1]

Contribute to the Code Base
===
Before you submit your Pull Request consider the following guidelines:

* Search <a href="https://github.com/Icenium/appbuilder-sublime-package/pulls">GitHub</a> for an open or closed Pull Request that relates to your submission. You don't want to duplicate effort.
* Make your changes in a new git branch:
```
    git checkout -b my-fix-branch master
```
* Create your patch.
* Commit your changes and create a descriptive commit message (the commit message is used to generate release notes):
```
    git commit -a
```
* Build your changes locally.
```
    grunt
```
> This will create 'Telerik AppBuilder.zip' which you will have to extract in the Sublime Text packages directory and ensure that the package is working properly.

* Push your branch to GitHub:
```
    git push origin my-fix-branch
```
* In GitHub, send a Pull Request to appbuilder-sublime-package:master.

* If we suggest changes then you can modify your branch, rebase and force a new push to your GitHub repository to update the Pull Request:
```
    git rebase master -i
    git push -f
```
* That's it! Thank you for your contribution!

When the patch is reviewed and merged, you can safely delete your branch and pull the changes from the main (upstream) repository:

* Delete the remote branch on GitHub:
```
    git push origin --delete my-fix-branch
```
* Check out the master branch:
```
    git checkout master -f
```
* Delete the local branch:
```
    git branch -D my-fix-branch
```
* Update your develop with the latest upstream version:
```
    git pull --ff upstream master
```

[Back to Top][1]

[1]: #contribute-to-the-telerik-appbuilder-package-for-sublime-text