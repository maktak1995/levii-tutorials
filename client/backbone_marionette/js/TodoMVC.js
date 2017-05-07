/*global Backbone, TodoMVC:true, $ */

import "../node_modules/todomvc-app-css/index.css";
import "../node_modules/todomvc-common/base.css";
import "../css/app.css";

var Mn = require('backbone.marionette');
var Backbone = require('backbone');
var App = require('./TodoMVC.Application');
var Router = require('./TodoMVC.Router');

$(function () {
	'use strict';
	var TodoMVCApp = App.TodoMVCApp();
	var TodoMVCRouter = Router.TodoMVCRouter();

	TodoMVCApp.on('start', function () {
		var controller = new TodoMVCRouter.Controller();
		controller.router = new TodoMVCRouter.Router({
			controller: controller
		});

		controller.start();
		Backbone.history.start();
	});

	TodoMVCApp.start();
});
