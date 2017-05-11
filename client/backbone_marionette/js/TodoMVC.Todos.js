/*global Backbone, TodoMVC:true */

var Backbone = require('backbone');
var BackboneLocalStorage = require('backbone.localstorage');

'use strict';

module.exports.Todo = Backbone.Model.extend({
	defaults: {
		title: '',
		completed: false,
		created: 0
	},

	initialize: function () {
		if (this.isNew()) {
			this.set('created', Date.now());
		}
	},

	toggle: function () {
		return this.set('completed', !this.isCompleted());
	},

	isCompleted: function () {
		return this.get('completed');
	},

	matchesFilter: function (filter) {
		if (filter === 'all') {
			return true;
		}

		if (filter === 'active') {
			return !this.isCompleted();
		}

		return this.isCompleted();
	}
});

module.exports.TodoList = Backbone.Collection.extend({
	model: module.exports.Todo,

	localStorage: new BackboneLocalStorage('todos-backbone-marionette'),

		comparator: 'created',

	getCompleted: function () {
		return this.filter(this._isCompleted);
	},

	getActive: function () {
		return this.reject(this._isCompleted);
	},

	_isCompleted: function (todo) {
		return todo.isCompleted();
	}
});
