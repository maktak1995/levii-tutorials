/*global Backbone */
var Backbone = require('backbone');
var BackboneRadio = require('backbone.radio');

(function () {
	'use strict';
	var filterState = new Backbone.Model({
		filter: 'all'
	});

	var filterChannel = BackboneRadio.channel('filter');
	filterChannel.reply('filterState', function () {
		return filterState;
	});
})();
