module.exports = function(grunt) {

  // Project configuration.
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),

    // Concatenate bower js and css files and place it in partyparrots/static folder
    bower_concat: {
      all: { 
        dest: {
	  js: 'partyparrots/static/js/bower.js',
          css: 'partyparrots/static/css/bower.css'
        },
     	mainFiles: {
	  'bootstrap': 'dist/css/bootstrap.css',
          'font-awesome': 'css/font-awesome.css'
      	}
      }
    },
    
    // Minify the js files
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
    },
  
    // Copy font files to partyparrots/static/fonts folder
    copy: {
      fonts: {
        files: [
          {
	    expand: true, cwd:'bower_components/font-awesome/fonts', src: ['**'], dest: 'partyparrots/static/fonts',
            expand: true, cwd:'bower_components/bootstrap/fonts', src: ['**'], dest: 'partyparrots/static/fonts',
	  }
        ]
      }
    } 
  });

  // Load the plugin to minify Javascript files
  grunt.loadNpmTasks('grunt-contrib-uglify');

  // Load the plugin that automatically imports every file ending in .js within bower_components directory
  grunt.loadNpmTasks('grunt-bower-concat');
  
  // Load the plugin to copy fonts from bower_components to static folder
  grunt.loadNpmTasks('grunt-contrib-copy');

  // Create a task to run bower_concat, minify the JS files, copy the font files
  grunt.registerTask('build_bower', ['bower_concat', 'uglify:bower', 'copy:fonts']);
}; 
