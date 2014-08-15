module.exports = function(grunt) {
    grunt.initConfig({
		copyPackageTo: "\\\\telerik.com\\Resources\\BlackDragon\\Builds\\appbuilder-sublime-package",
		
        movePackageTo: process.env["JOB_NAME"] ? "\\\\telerik.com\\Resources\\BlackDragon\\Builds\\appbuilder-sublime-package" : "build",
        jobName: process.env["JOB_NAME"] || "local",
        buildNumber: process.env["BUILD_NUMBER"] || "non-ci",
        destinationFolder: process.env["JOB_NAME"] ? "<%= movePackageTo %>\\<%= jobName %>\\<%= grunt.template.today('yyyy-mm-dd') %> #<%= buildNumber %>" : "<%= movePackageTo %>",

        compress: {
            main: {
                options: {
                    archive: "<%= destinationFolder %>\\Telerik AppBuilder.zip"
                },
                files: [
                    { src: ["**/*.{py,pyd,so}", "*.{sublime-keymap,sublime-menu,sublime-settings}", "LICENSE"] }
                ]
            }
        },
		
		copy: {
			package_to_qa_drop_folder: {
				src: "*<%= destinationFolder %>\\Telerik AppBuilder.zip",
				dest: "<%= copyPackageTo %>\\<%= jobName %>\\Telerik AppBuilder.zip"
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