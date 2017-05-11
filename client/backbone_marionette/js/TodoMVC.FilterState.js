/*global Backbone */
var Backbone = require('backbone');

var filter = function () {
	'use strict';
	var filterState = new Backbone.Model({
		filter: 'all'
	});

	var filterChannel = Backbone.Radio.channel('filter');
	filterChannel.reply('filterState', function () {
		return filterState;
	});
};

module.exports = filter();
