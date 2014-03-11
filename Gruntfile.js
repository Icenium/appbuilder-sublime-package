module.exports = function(grunt) {
    grunt.initConfig({
        copyPackageTo: "\\\\telerik.com\\Resources\\BlackDragon\\Builds\\appbuilder-sublime-package",
        jobName: process.env["JOB_NAME"] || "local",
        buildNumber: process.env["BUILD_NUMBER"] || "non-ci",
        subFolder: "<%= jobName %>\\<%= grunt.template.today('yyyy-mm-dd') %> #<%= buildNumber %>",

        compress: {
            main: {
                options: {
                    archive: "<%= copyPackageTo %>\\<%= subFolder %>\\AppBuilder.zip"
                },
                files: [
                    { src: ["**/*.{py,pyd,so}", "*.{sublime-keymap,sublime-menu,sublime-settings}", "LICENSE"] }
                ]
            }
        },

        clean: {
            src: ["**/*.pyc"]
        }
    });

    grunt.loadNpmTasks("grunt-contrib-compress");
    grunt.loadNpmTasks("grunt-contrib-clean");
    grunt.registerTask("default", "compress:main");
}