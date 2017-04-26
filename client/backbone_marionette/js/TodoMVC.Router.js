/*global TodoMVC:true, Backbone, $ */

var TodoMVC = TodoMVC || {};

(function(){
    'use strict';

    var filterChannel = Backbone.Radio.channel('filter');

    TodoMVC.Router = Mn.AppRouter.extend({
        appRoutes: {
            '*filter': 'filterItems'
        }
    });

    TodoMVC.controller = Mn.Object.extend({
        initialize: function () {
            this.todoList = new TodoMVC.TodoList();
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
            var header = new TodoMVC.HeaderLayout({
                collection: todoList
            });
            TodoMVC.App.root.showChildView('header', header);
        },

        showFooter: function (todoList) {
            var footer = new TodoMVC.FooterLayout({
                collection: todoList
            });
            TodoMVC.App.root.showChildView('footer', footer);
        },

        showTodoList: function (todoList) {
            TodoMVC.App.root.showChildView('main', new TodoMVC.LisiView({
                collection: todoList
            }));
        },

        filterItems: function (filter) {
            var newFilter = filter && filter.trim() || 'all';
            filterChannel.request('filterState').set('filter', newFilter);
        }
    });
})();
