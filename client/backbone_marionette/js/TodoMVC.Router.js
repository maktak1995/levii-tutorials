/*global TodoMVC:true, Backbone, $ */
var Mn = require('backbone.marionette');
var Backbone = require('backbone');
var BackboneRadio = require('backbone.radio');
var App = require('./TodoMVC.Application');
var Layout = require('./TodoMVC.Layout');
var Todos = require('./TodoMVC.Todos');
var TodoView = require('./TodoMVC.TodoList.Views');
var Filter = require('./TodoMVC.FilterState');

var TodoMVCRouter = function () {
	'use strict';

	var TodoMVC = {};

	var filterChannel = BackboneRadio.channel('filter');

	TodoMVC.Router = Mn.AppRouter.extend({
		appRoutes: {
			'*filter': 'filterItems'
		}
	});

	TodoMVC.Controller = Mn.Object.extend({

		initialize: function () {
			this.todoList = new Todos.TodoList();
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
			var header = new Layout.HeaderLayout({
				collection: todoList
			});
			App.root.showChildView('header', header);
		},

		showFooter: function (todoList) {
			var footer = new Layout.FooterLayout({
				collection: todoList
			});
			App.root.showChildView('footer', footer);
		},

		showTodoList: function (todoList) {
			App.root.showChildView('main', new TodoView.ListView({
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

module.exports = TodoMVCRouter();
