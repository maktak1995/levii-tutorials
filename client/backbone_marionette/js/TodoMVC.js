/*global Backbone, TodoMVC:true, $ */

var TodoMVC = TodoMVC || {};

$(function () {
	'use strict';

	TodoMVC.App.on('start', function () {
		var controller = new TodoMVC.Controller();
		controller.router = new TodoMVC.Router({
			controller: controller
		});

		controller.start();
		Backbone.history.start();
	});

	TodoMVC.App.start();
});
