module.exports = {    
    settings: {
      "vetur.useWorkspaceDependencies": true,
      "vetur.experimental.templateInterpolationService": true
    },
    
    projects: [
      './web_app', 
      {        
        root: './web_app',       
        package: './web_app/package.json',        
        tsconfig: './web_app/tsconfig.json',               
        globalComponents: [
          './web_app/src/components/**/*.vue'
        ]
      }
    ]
  }