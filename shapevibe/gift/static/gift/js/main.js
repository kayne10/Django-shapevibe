var GiftList = {
	init: function() {
		this.$container = $('.gift-list');
		this.render();
		this.bindEvents();
	},

	render: function() {

	}
};

var UserList = {
	init: function() {
		this.$container = $('.user-list');
		this.render();
		this.bindEvents();
	},

	render: function() {

	}
};

$(document).ready(function() {
	AlbumsListPage.init();
	SongsListPage.init();
});