/*global TodoMVC:true, Backbone */
var Mn = require('backbone.marionette');
var Backbone = require('backbone');
var Radio = require('backbone.radio');
var Filter = require('./TodoMVC.FilterState');

'use strict';

var filterChannel = Backbone.Radio.channel('filter');

module.exports.RootLayout = Mn.View.extend({

	el: '#todoapp',

	regions: {
		header: '#header',
		main: '#main',
		footer: '#footer'
	}
});

module.exports.HeaderLayout = Mn.View.extend({

	template: '#template-header',

	ui: {
		input: '#new-todo'
	},

	events: {
		'keypress @ui.input': 'onInputKeypress',
		'keyup @ui.input': 'onInputKeyup'
	},

	onInputKeyup: function (e) {
		var ESC_KEY = 27;

		if (e.which === ESC_KEY) {
			this.render();
		}
	},

	onInputKeypress: function (e) {
		var ENTER_KEY = 13;
		var todoText = this.ui.input.val().trim();

		if (e.which === ENTER_KEY && todoText) {
			this.collection.create({
				title: todoText
			});
			this.ui.input.val('');
		}
	}
});


module.exports.FooterLayout = Mn.View.extend({
	template: '#template-footer',

	ui: {
		filters: '#filters a',
		completed: '.completed a',
		active: '.active a',
		all: '.all a',
		summary: '#todo-count',
		clear: '#clear-completed'
	},

	events: {
		'click @ui.clear': 'onClearClick'
	},

	collectionEvents: {
		all: 'render'
	},

	templateContext: {
		activeCountLabel: function () {
			return (this.activeCount === 1 ? 'item' : 'items') + ' left';
		}
	},

	initialize: function () {
		this.listenTo(filterChannel.request('filterState'), 'change:filter', this.updateFilterSelection, this);
	},

	serializeData: function () {
		var active = this.collection.getActive().length;
		var total = this.collection.length;

		return {
			activeCount: active,
			totalCount: total,
			completedCount: total - active
		};
	},

	onRender: function () {
		this.$el.parent().toggle(this.collection.length > 0);
		this.updateFilterSelection();
	},

	updateFilterSelection: function () {
		this.ui.filters.removeClass('selected');
		this.ui[filterChannel.request('filterState').get('filter')]
		.addClass('selected');
	},

	onClearClick: function () {
		var completed = this.collection.getCompleted();
		completed.forEach(function (todo) {
			todo.destroy();
		});
	}
});
