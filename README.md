Sublime Text Package for Telerik AppBuilder by Progress
==========================

*Build and test iOS, Android and Windows Phone apps using a single pure HTML5, CSS, and JavaScript code base*

[![Telerik AppBuilder](https://raw.githubusercontent.com/Icenium/appbuilder-sublime-package/master/ab-logo.png "Telerik AppBuilder")](http://www.telerik.com/appbuilder "The Telerik AppBuilder web site")

**Leverage the build and test capabilities of AppBuilder from Sublime Text 2 or Sublime Text 3**

This package lets you run your mobile app on connected devices or in the device simulator, and synchronize your code changes to the running app without redeploying it. The package requires that the Telerik AppBuilder Command-Line Interface by Progress is installed on your system.

> The AppBuilder Command-Line Interface is delivered for Windows, OS X, and Linux as an npm package. For more information click <a href="https://www.npmjs.org/package/appbuilder" target="_blank">here</a>.

* [Installation](#installation "How to install the AppBuilder package for Sublime Text")
* [Usage](#usage "How to build, deploy, and sync your apps from Sublime Text")
* [Contribution](#contribution "How to help improve the AppBuilder package for Sublime Text")
* [More AppBuilder Tools and Resources](#more-telerik-appbuilder-tools-and-resources "Learn more about the available AppBuilder tools and resources")
* [License](#license "Licensing information about the AppBuilder package for Sublime Text")

Installation
===

Latest version: AppBuilder 3.5
Release date: September 20, 2016

> For a complete list of the improvements and updates available in this release, see <a href="http://docs.telerik.com/platform/appbuilder/release-notes/v3-5" target="_blank">AppBuilder 3.5 Release Notes</a>.

### Software Requirements

* Windows, OS X Yosemite or later, or Linux
* Sublime Text 2 or Sublime Text 3
* Package Control for your version of Sublime Text
* AppBuilder Command-Line Interface<br/>Your version of the AppBuilder package for Sublime Text must match the latest official major release of the AppBuilder Command-Line Interface.
* Any software required by the <a href="https://www.npmjs.org/package/appbuilder" target="_blank">AppBuilder Command-Line Interface</a>

### Install the Package

Install this package with <a href="http://wbond.net/sublime_packages/package_control" target="_blank">Package Control</a>.

* [Install the AppBuilder Package for Sublime Text on Windows](#install-the-appbuilder-package-for-sublime-text-on-windows "Install the AppBuilder package for Sublime Text on Windows")
* [Install the AppBuilder Package for Sublime Text on OS X](#install-the-appbuilder-package-for-sublime-text-on-os-x "Install the AppBuilder package for Sublime Text on OS X")
* [Install the AppBuilder Package for Sublime Text on Linux](#install-the-appbuilder-package-for-sublime-text-on-linux "Install the AppBuilder package for Sublime Text on Linux")

#### Install the AppBuilder package for Sublime Text on Windows

1. Run Sublime Text.
1. Select **Preferences** &#8594; **Package Control**.
1. Select **Install Package**.
1. Start typing *AppBuilder* and select the package from the list.
1. Wait for the installation to complete.

#### Install the AppBuilder package for Sublime Text on OS X

1. Run Sublime Text.
1. Select **Sublime Text** &#8594; **Preferences** &#8594; **Package Control**.
1. Select **Install Package**.
1. Start typing *AppBuilder* and select the package from the list.
1. Wait for the installation to complete.

If Sublime Text cannot load the package properly, verify that the path variables for Node.js and AppBuilder are populated properly in `telerik_appbuilder.sublime-settings`.

1. In the terminal, run the following command.

    ```Shell
    which node
    ```
1. In the terminal, run the following command.

    ```Shell
    which appbuilder
    ```
1. Select **Sublime Text** &#8594; **Preferences** &#8594; **Browse packages...**.
1. If not present, create the **AppBuilder** folder.
1. Open the **AppBuilder** folder.
1. If not present, create a `telerik_appbuilder.sublime-settings` file.
1. Open `telerik_appbuilder.sublime-settings` and replace the declared path values.

    ```
    {
        "node_osx_path": "The path retrieved in Step 1",
        "appbuilder_osx_path": "The path retrieved in Step 2"
    }
    ```
1. Save changes.
1. Restart Sublime Text.

#### Install the AppBuilder package for Sublime Text on Linux

1. Run Sublime Text.
1. Select **Sublime Text** &#8594; **Preferences** &#8594; **Package Control**.
1. Select **Install Package**.
1. Start typing *AppBuilder* and select the package from the list.
1. Wait for the installation to complete.

If Sublime Text cannot load the package properly, verify that the path variables for Node.js and AppBuilder are populated properly in `telerik_appbuilder.sublime-settings`.

1. In the terminal, run the following command.

    ```Shell
    which node
    ```
1. In the terminal, run the following command.

    ```Shell
    which appbuilder
    ```
1. Select **Sublime Text** &#8594; **Preferences** &#8594; **Browse packages...**.
1. If not present, create the **AppBuilder** folder.
1. Open the **AppBuilder** folder.
1. If not present, create a `telerik_appbuilder.sublime-settings` file.
1. Open `telerik_appbuilder.sublime-settings` and replace the declared path values.

    ```
    {
        "linux_node_path": "The path retrieved in Step 1",
        "linux_appbuilder_path": "The path retrieved in Step 2"
    }
    ```
1. Save changes.
1. Restart Sublime Text.

The Telerik AppBuilder menu becomes available under the **Tools** menu.

[Back to Top][1]

Usage
===

After you install this package, you can access the available build and sync commands from **Tools** -> **Telerik AppBuilder**.

* [Run on Device](#run-on-device "Build and deploy to device")
* [Configure LiveSync](#configure-livesync "Configure LiveSync")
* [Reload the App on Device](#reload-the-app-on-device "Reload the running app on device")
* [Run in the Device Simulator](#run-in-the-device-simulator "Deploy in the device simulator")

### Run on Device

You can build and deploy your app on one device at a time with the **Tools** -> **Telerik AppBuilder** -> **Build and Deploy** operation.

> In this version of the AppBuilder package for Sublime Text for Linux, you cannot build and deploy your app via cable connection on iOS devices.

> To be able to work with connected iOS devices on Windows systems, verify that you have downloaded and installed the 32-bit Node.js.

1. Connect your devices.
1. Select **Tools** -> **Telerik AppBuilder** -> **Build and Deploy**.<br/>If you have connected multiple devices, Sublime Text will display a drop-down list of the connected devices with their unique identifiers and mobile platform.
1. If prompted, select the device on which you want to deploy.
1. Track the deployment process in the status bar and in the log.
1. After the deployment completes, run your app on device.

### Configure LiveSync

You can toggle real-time synchronization of your code changes on save with the **Tools** -> **Telerik AppBuilder** -> **LiveSync on Save** option.

When you modify your code and save your changes, your running app will refresh automatically if the device is connected to your system. This operation replaces only the modified application files.

1. Select **Tools** -> **Telerik AppBuilder** -> **Enable LiveSync on Save**.<br/>A check mark indicates that LiveSync is enabled.
1. On your connected devices or in the device simulator, run your app.
1. Modify your code and save changes.

The app refreshes automatically.

<a name="sync"></a>
### Reload the App on Device

You can synchronize all your changes to an app deployed on a connected device at once with the **Tools** -> **Telerik AppBuilder** -> **LiveSync Application** operation. This operation replaces all application files at once.

> In this version of the AppBuilder package for Sublime Text for Linux, you cannot LiveSync your app via cable connection on iOS devices.

> To be able to work with connected iOS devices on Windows systems, verify that you have downloaded and installed the 32-bit Node.js.

1. Verify that you have connected your device and you have deployed the app.
1. Run your app.
1. Modify your code and save changes.
1. Select **Tools** -> **Telerik AppBuilder** -> **LiveSync Application**.<br/>If you have connected multiple devices, Sublime Text will display a drop-down list of the connected devices with their unique identifiers and mobile platform.
1. Select the device to which you want to sync changes.
1. Track the deployment process in the status bar and in the log.

<a name="simulator"></a>
### Run in the Device Simulator

You can build and deploy your app in the device simulator with the **Tools** -> **Telerik AppBuilder** -> **Run in Simulator** operation.

> In this version of the AppBuilder package for Sublime Text for Linux, you cannot run your app in the device simulator.

* Select **Tools** -> **Telerik AppBuilder** -> **Run in Simulator**.

In the device simulator, you can change the target device form factor, mobile platform and version, and orientation. You can adjust the geolocation details, network connection configuration, file storage configuration, and the default contacts. You can debug your code using the built-in debug tools.

[Back to Top][1]

<a name="contribute"></a>Contribution
===

To learn how to log a bug that you just discovered, click [here](CONTRIBUTING.md#report-an-issue).

To learn how to suggest a new feature or improvement, click [here](CONTRIBUTING.md#request-a-feature).

To learn how to contribute to the code base, click [here](CONTRIBUTING.md#contribute-to-the-code-base).

[Back to Top][1]

<a name="more"></a>More AppBuilder Tools and Resources
===

* [AppBuilder Windows client](http://www.telerik.com/appbuilder/windows-client "The AppBuilder Windows Client"): Lightweight Windows IDE.
* [AppBuilder in-browser client](http://www.telerik.com/appbuilder/in-browser-client "The AppBuilder In-Browser Client"): Browser-based IDE that is compatible with most modern web and mobile browsers.
* [AppBuilder extension for Visual Studio](http://www.telerik.com/appbuilder/visual-studio-extension "The AppBuilder Extension for Visual Studio"): Extension for the popular Microsoft IDE.
* [AppBuilder command-line interface](http://www.telerik.com/appbuilder/command-line-interface "The AppBuilder command-line interface"): A command-line interface that lets you leverage the cloud capabilities of AppBuilder from the command line.
* [AppBuilder companion app](http://www.telerik.com/appbuilder/companion-app "The AppBuilder Companion App"): iOS, Android and Windows Phone testing utility <a href="https://itunes.apple.com/bg/app/icenium-ion/id527547398" target="_blank">available for free on the App Store</a>.
* [AppBuilder documentation](http://docs.telerik.com/platform/appbuilder "The documentation resources for AppBuilder"): Learn more about what you can do with AppBuilder.
* [AppBuilder web page](http://www.telerik.com/appbuilder "The AppBuilder web page"): Visit the AppBuilder web site.

[Back to Top][1]

<a name="license"></a>License
===

This software is licensed under the Apache 2.0 license, quoted <a href="LICENSE" target="_blank">here</a>.

[Back to Top][1]

[1]: #telerik-appbuilder-for-sublime-text
