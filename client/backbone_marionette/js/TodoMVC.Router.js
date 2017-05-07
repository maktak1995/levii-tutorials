/*global TodoMVC:true, Backbone, $ */
var Mn = require('backbone.marionette');
var Backbone = require('backbone');
var BackboneRadio = require('backbone.radio');
var App = require('./TodoMVC.Application');
var Layout = require('./TodoMVC.Layout');
var Todos = require('./TodoMVC.Todos');
var TodoView = require('./TodoMVC.TodoList.Views');

var TodoMVCRouter = function () {
	'use strict';

	var TodoMVC = {};
	var TodoMVCTodos = Todos.TodoMVCTodos();
	var TodoMVCLayout = Layout.TodoMVCLayout();
	var TodoMVCApp = App.TodoMVCApp();
	var TodoMVCTodoView = TodoView.TodoMVCTodoView();

	var filterChannel = BackboneRadio.channel('filter');

	TodoMVC.Router = Mn.AppRouter.extend({
		appRoutes: {
			'*filter': 'filterItems'
		}
	});

	TodoMVC.Controller = Mn.Object.extend({

		initialize: function () {
			this.todoList = new TodoMVCTodos.TodoList();
		},

		start: function () {
			this.showHeader(this.todoList);
			this.showFooter(this.todoList);
			this.showTodoList(this.todoList);
			this.todoList.on('all', this.updateHiddenElements, this);
			this.todoList.fetch();
		},

		updateHiddenElements: function () {
			$('#main, #footer').toggle(!!this.todoList.length);
		},

		showHeader: function (todoList) {
			var header = new TodoMVCLayout.HeaderLayout({
				collection: todoList
			});
			TodoMVCApp.root.showChildView('header', header);
		},

		showFooter: function (todoList) {
			var footer = new TodoMVCLayout.FooterLayout({
				collection: todoList
			});
			TodoMVCApp.root.showChildView('footer', footer);
		},

		showTodoList: function (todoList) {
			TodoMVCApp.root.showChildView('main', new TodoMVCTodoView.ListView({
				collection: todoList
			}));
		},

		filterItems: function (filter) {
			var newFilter = filter && filter.trim() || 'all';
			filterChannel.request('filterState').set('filter', newFilter);
		}
	});

	return TodoMVC;
};

exports.TodoMVCRouter = TodoMVCRouter;
