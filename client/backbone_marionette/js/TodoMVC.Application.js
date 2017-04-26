/* global Backbone, TodoMVC:true */

var TodoMVC = TodoMVC || {};

(function () {
    'use strict';

    var TodoApp = Mn.Application.extend({
        setRootLayout: function () {
            this.root = new TodoMVC.RootLayout();
        }
    });

    TodoMVC.App = new TodoApp();

    TodoMVC.App.on('before:start', function (){
        TodoMVC.App.setRootLayout();
    });
})();
