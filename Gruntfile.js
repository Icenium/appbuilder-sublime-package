module.exports = function(grunt) {
    grunt.initConfig({

        destinationFolder: "build_output",

        compress: {
            main: {
                options: {
                    archive: "<%= destinationFolder %>\\AppBuilder.zip"
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
