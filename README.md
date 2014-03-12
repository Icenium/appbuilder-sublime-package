Telerik AppBuilder for Sublime Text 2
==========================

*Build and test iOS and Android hybrid apps using a single pure HTML5, CSS, and JavaScript code base*

[![Telerik AppBuilder](ab-logo.png "Telerik AppBuilder")](http://www.telerik.com/appbuilder "The Telerik AppBuilder web site")

**Leverage the build and test capabilities of Telerik AppBuilder from Sublime Text 2**

This package lets you run your hybrid mobile app on connected devices or in the device simulator, and synchronize your code changes to the running app without redeploying it. The package requires that the Telerik AppBuilder Command-Line Interface is installed on your system.

* [Installation](#install "How to install the Telerik AppBuilder package for Sublime Text 2")
* [Usage](#usage "How to build, deploy, and sync your apps from Sublime Tex 2")
* [Contribution](#contribute "How to help improve the Telerik AppBuilder package for Sublime")
* [More Telerik AppBuilder Tools and Resources](#more "Learn more about the available Telerik AppBuilder tools and resources")
* [License](#license "Licensing information about the Telerik AppBuilder package for Sublime Text 2")

<a id="installation"></a>Installation
===

### Software Requirements

* Windows or OS X Mavericks
* Sublime Text 2
* Telerik AppBuilder Command-Line Interface
* Any software required by the <a href="https://www.npmjs.org/package/appbuilder" target="_blank">Telerik AppBuilder Command-Line Interface</a>

### Install the Package

Install this package with <a href="http://wbond.net/sublime_packages/package_control" target="_blank">Package Control</a>.

[Back to Top][1]

<a id="usage"></a>Usage
===

After you install this package, you can access the available build and sync commands from **Tools** -> **Telerik AppBuilder**.

* [Run on Device](#device "Build and deploy to device")
* [Run in the Device Simulator](#simulator "Deploy in the device simulator")
* [Configure LiveSync](#livesync "Configure LiveSync")
* [Reload the App on Device](#sync "Reload the running app on device")

<a id="device"></a>
### Run on Device

You can build and deploy your app on one device at a time with the **Tools** -> **Telerik AppBuilder** -> **Build and Deploy** operation.

1. Connect your devices.
1. Select **Tools** -> **Telerik AppBuilder** -> **Build and Deploy**.<br/>If you have connected multiple devices, Sublime Text 2 will display a drop-down list of the connected devices with their unique identifiers and mobile platform.
1. If prompted, select the device on which you want to deploy.
1. Track the deployment process in the status bar and in the log.
1. After the deployment completes, run your app on device.

<a id="livesync"></a>
### Configure LiveSync

You can toggle real-time synchronization of your code changes on save with the **Tools** -> **Telerik AppBuilder** -> **LiveSync on Save** option. 

When you modify your code and save your changes, your running app will refresh automatically if the device is connected to your system. This operation replaces only the modified application files.

1. Select **Tools** -> **Telerik AppBuilder** -> **LiveSync on Save**.<br/>A check box indicates that LiveSync is enabled.
1. On your connected devices or in the device simulator, run your app.
1. Modify your code and save changes.

The app refreshes automatically.

<a id="sync"></a>
### Reload the App on Device

You can synchronize all your changes to an app deployed on a connected device at once with the **Tools** -> **Telerik AppBuilder** -> **LiveSync Application** operation. This operation replaces all application files at once.

1. Verify that you have connected your device and you have deployed the app.
1. Run your app.
1. Modify your code and save changes.
1. Select **Tools** -> **Telerik AppBuilder** -> **LiveSync Application**.<br/>If you have connected multiple devices, Sublime Text 2 will display a drop-down list of the connected devices with their unique identifiers and mobile platform.
1. Select the device to which you want to sync changes.
1. Track the deployment process in the status bar and in the log.

<a id="simulator"></a>
### Run in the Device Simulator (Available only on Windows)

You can build and deploy your app in the device simulator with the **Tools** -> **Telerik AppBuilder** -> **Run in Simulator** operation. 

* Select **Tools** -> **Telerik AppBuilder** -> **Run in Simulator**.

In the device simulator, you can change the target device form factor, mobile platform and version, and orientation. You can adjust the geolocation details, network connection configuration, file storage configuration, and the default contacts. You can debug your code using the built-in debug tools.

[Back to Top][1]

<a id="contribute"></a>Contribution
===

To learn how to log a bug that you just discovered, click [here](CONTRIBUTE#bug).

To learn how to suggest a new feature or improvement, click [here](CONTRIBUTE#request).

To learn how to contribute to the code base, click [here](CONTRIBUTE#contribute).

[Back to Top][1]

<a id="more"></a>More Telerik AppBuilder Tools and Resources
===

* [Telerik AppBuilder Windows client](http://www.telerik.com/appbuilder/windows-client "The AppBuilder Windows Client"): Lightweight Windows IDE.
* [Telerik AppBuilder in-browser client](http://www.telerik.com/appbuilder/in-browser-client "The AppBuilder In-Browser Client"): Browser-based IDE that is compatible with most modern web and mobile browsers.
* [Telerik AppBuilder extension for Visual Studio](http://www.telerik.com/appbuilder/visual-studio-extension "The AppBuilder Extension for Visual Studio"): Extension for the popular Microsoft IDE.
* [Telerik AppBuilder command-line interface](??? "The AppBuilder package for Sublime Text 2"): A command-line interface that lets you leverage the cloud capabilities of Telerik AppBuilder from the command line.
* [Telerik AppBuilder companion app](http://www.telerik.com/appbuilder/companion-app "The AppBuilder Companion App"): iOS testing utility <a href="https://itunes.apple.com/bg/app/icenium-ion/id527547398" target="_blank">available for free on the App Store</a>.
* [Telerik AppBuilder documentation](http://docs.telerik.com/platform/appbuilder "The documentation resources for Telerik AppBuilder"): Learn more about what you can do with Telerik AppBuilder.
* [Telerik AppBuilder web page](http://www.telerik.com/appbuilder "The Telerik AppBuilder web page"): Visit the Telerik AppBuilder web site.

[Back to Top][1]

<a id="license"></a>License
===

This software is licensed under the Apache 2.0 license, quoted <a href="LICENSE" target="_blank">here</a>.

[Back to Top][1]

[1]: #telerik-appbuilder-for-sublime-text-2
