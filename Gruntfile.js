module.exports = function(grunt) {

  // Project configuration.
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),
    bower_concat: {
      all: { 
        dest: 'partyparrots/static/js/bower.js'
      }
    },
    
    uglify: {
      bower: {
        options: {
          mangle: true,
          compress: true
        },
        files: {
          'partyparrots/static/js/bower.min.js': 'partyparrots/static/js/bower.js'
        }
      }
    }
  });

  // Load the plugin to minify Javascript files
  grunt.loadNpmTasks('grunt-contrib-uglify');

  // Load the plugin that automatically imports every file ending in .js within bower_components directory
  grunt.loadNpmTasks('grunt-bower-concat');

  // Create a task to run bower_concat and uglify the js file
  grunt.registerTask('build_bower', ['bower_concat', 'uglify:bower']);

}; 
