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

function revealSearchBar() {
    var x = document.getElementById("indexSearch");
    if (x.style.display === 'none'){
        x.style.display = "block";
    } else {
        x.style.display = "none";
    }
}