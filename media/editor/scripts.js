function Data(url, type) {
  this.data = [];
  this.page = 0;
  this.url = url;
  this.type = type;
};
Data.prototype.pageUrl = function(page) {
  return this.url + '/' + page + '/';
};
Data.prototype.update = function(page, clbk) {
  if (this.data[page]) {
    if (clbk) clbk();
    return;
  }
	var self = this;
  $.getJSON(this.pageUrl(page), function(data) {
    self.data[page] = data;
    if (clbk) clbk();
  });
};
Data.prototype.reset = function() {
  this.data = [];
};
Data.prototype.render = function() {
  var $el = $("#insert .content");
  $el.html("");
  for (i = 0; i < this.data[this.page].length; i++)
    this.renderItem(this.data[this.page][i]).appendTo($el);
};
Data.prototype.renderItem = function(item) {
  var $el = $("<div/>").addClass('inserter').data('item', item).text(item.title);
  $("<img/>").attr("src", item.thumbnail).css("float", "left").appendTo($el);
	$("<div style='clear: both'></div>").appendTo($el);
  return $el;
};
Data.prototype.renderItemForEditor = function(item) {
	return $("<img/>")
	.attr("src", item.thumbnail)
	.attr("title", item.title)
	.attr("data-type", item.type)
	.attr("data-id", item.id);
};

window.app = {
	Image: new Data('images', 'image'),
	Video: new Data('videos', 'video'),
	current: null,
	show_images: function() {
		app.current = app.Image;
		app.current.update(app.current.page, function() {
			app.current.render();
		});
		$("#page_actions").show();
	},
	show_videos: function() {
		app.current = app.Video;
		app.current.update(app.current.page, function() {
			app.current.render();
		});
		$("#page_actions").show();
	}
};

$(function() {
  $("#editor").trumbowyg({
    lang: 'fa',
		autogrow: true
  });
  $("#save_button").on('click', function() {
    $("#save_message").text('Saving...');
    $.ajax({
      type: "post",
      url: "save/",
      data: {
        'source': $("#editor").trumbowyg('html')
      },
      success: function() {
        $("#save_message").text('');
      },
      error: function() {
        $("#save_message").text('Error!');
      }
    });
  });
	$("#show_images").on('click', app.show_images);
	$("#show_videos").on('click', app.show_videos);
	$("#insert .content").on('click', 'div.inserter', function() {
		$("#editor").trumbowyg("insertMedia", 
				app.current.renderItemForEditor($(this).data('item')));
	});
});
