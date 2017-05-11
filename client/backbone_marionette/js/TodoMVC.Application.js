/*global Backbone, TodoMVC:true */

var Mn = require('backbone.marionette');
var Backbone = require('backbone');
var Layout = require('./TodoMVC.Layout');

'use strict';

var TodoApp = Mn.Application.extend({
	setRootLayout: function () {
		this.root = new Layout.RootLayout();
	}
});

var TodoMVCApp = new TodoApp();

TodoMVCApp.on('before:start', function () {
	TodoMVCApp.setRootLayout();
});

module.exports = TodoMVCApp;
