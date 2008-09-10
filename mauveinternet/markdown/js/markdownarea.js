Event.observe(document, 'dom:loaded', function () {
	
	$$('textarea.markdown').each(function (t) {
		var converter = new Showdown.converter;  
		var preview = new Element('div', {'class': 'markdown_preview'}).update(converter.makeHtml(t.getValue()));
		t.insert({before: preview});

		var area = new Control.TextArea(t);
		var toolbar = new Control.TextArea.ToolBar(area);  
		toolbar.container.className = 'markdown_toolbar';

		//preview of markdown text  
		area.observe('change', function(value){  
			var start = area.getSelectionStart();
			var src = area.getValue();

			src = src.substr(0, start) + '<span class="caret"></span>' + src.substr(start);
//			var pbreak = src.lastIndexOf('\n\n', start);
//			
//			if (pbreak == -1)
//				pbreak = src.lastIndexOf('\r\n\r\n', start);
//
//			if (pbreak != -1)
//			{
//				//insert a marker that we can find later
//				src = src.substr(0, pbreak) + '\n\n<div class="sel"></div>' + src.substr(pbreak);
//			}
			preview.update(converter.makeHtml(src));
			var sel = preview.select('.caret')[0];
			if (sel)
			{
				preview.scrollTop = sel.cumulativeOffset().top - preview.cumulativeOffset().top - 30;
			}
		}); 
		  
		toolbar.addButton('Bold',function(){  
			this.wrapSelection('**','**');  
		},{  
			className: 'markdown_bold_button',
			title: 'Bold'
		});  

		//buttons  
		toolbar.addButton('Italics',function(){  
			this.wrapSelection('*','*');  
		},{  
			className: 'markdown_italic_button',
			title: 'Italic'  
		});  
		  
		toolbar.addButton('Link',function(){
			LinkDialog.init(area);
			return;
			var selection = this.getSelection();  
			var response = prompt('Enter Link URL','');  
			if(response == null)  
				return;  
			this.replaceSelection('[' + (selection == '' ? 'Link Text' : selection) + '](' + (response == '' ? 'http://link_url/' : response).replace(/^(?!(f|ht)tps?:\/\/)/,'http://') + ')');  
		},{  
			className: 'markdown_link_button',
			title: 'Insert Link'
		});  
		  
//		toolbar.addButton('Image',function(){  
//			var selection = this.getSelection();  
//			var response = prompt('Enter Image URL','');  
//			if(response == null)  
//				return;  
//			this.replaceSelection('![' + (selection == '' ? 'Image Alt Text' : selection) + '](' + (response == '' ? 'http://image_url/' : response).replace(/^(?!(f|ht)tps?:\/\/)/,'http://') + ')');  
//		},{  
//			className: 'markdown_image_button',
//			title: 'Insert Image'
//		});  
		  
		toolbar.addButton('Heading',function(){  
			var selection = this.getSelection();  
			if(selection == '')  
				selection = 'Heading';  
			this.replaceSelection("\n" + selection + "\n" + $R(0,Math.max(5,selection.length)).collect(function(){'-'}).join('') + "\n");  
		},{  
			className: 'markdown_heading_button',
			title: 'Heading'  
		});  
		  
		toolbar.addButton('Unordered List',function(event){  
			this.collectFromEachSelectedLine(function(line){  
				return event.shiftKey ? (line.match(/^\*{2,}/) ? line.replace(/^\*/,'') : line.replace(/^\*\s/,'')) : (line.match(/\*+\s/) ? '*' : '* ') + line;  
			});  
		},{  
			className: 'markdown_unordered_list_button',
			title: 'Unordered List' 
		});  
		  
		toolbar.addButton('Ordered List',function(event){  
			var i = 0;  
			this.collectFromEachSelectedLine(function(line){  
				if(!line.match(/^\s+$/)){  
					++i;  
					return event.shiftKey ? line.replace(/^\d+\.\s/,'') : (line.match(/\d+\.\s/) ? '' : i + '. ') + line;  
				}  
			});  
		},{  
			className: 'markdown_ordered_list_button', 
			title: 'Ordered List'
		});  
		  
//		toolbar.addButton('Block Quote',function(event){  
//			this.collectFromEachSelectedLine(function(line){  
//				return event.shiftKey ? line.replace(/^\> /,'') : '> ' + line;  
//			});  
//		},{  
//			className: 'markdown_quote_button'  
//		});  
	});
});

var LinkDialog = {
	init: function(textarea) {
		LinkDialog.textarea = textarea;
		var cont = new Element('div', {id: 'link-dialog'});

		cont.update('<p>Please select what you would like to link to:</p>' +
'<p><input type="radio" name="link-dialog-type" id="link-dialog-type-internal" value="internal" checked="checked"/> <label for="link-dialog-type-internal">A page within this site</label>' +
'<select id="link-dialog-model"></select><select id="link-dialog-inst"></select></p>' +
'<p><input type="radio" name="link-dialog-type" id="link-dialog-type-external" value="external" /> <label for="link-dialog-type-external">Another site on the web</label>' +
'<input type="text" id="link-dialog-abslink" value="http://" /></p>' +
'<div class="buttons"><button id="link-dialog-insert">Insert</button><button id="link-dialog-cancel">Cancel</button></div>'
);
		document.body.appendChild(cont);
		var at = $(textarea.element).cumulativeOffset();
		cont.setStyle({left: (at.left + (textarea.element.offsetWidth - cont.offsetWidth)/2) + 'px', top: (at.top + (textarea.element.offsetHeight - cont.offsetHeight)/2) + 'px'});
		new Ajax.Request('/admin/markdown/links', {method: 'GET'})
		LinkDialog.modelwatcher = new Form.Element.Observer('link-dialog-model', 0.2, LinkDialog.refreshInstances);
		Event.observe('link-dialog-insert', 'click', LinkDialog.insertAndClose);
		Event.observe('link-dialog-cancel', 'click', LinkDialog.close);
	},

	insertAndClose: function () {
		if ($('link-dialog-type-internal').checked) {
			var link = 'internal:' + $F('link-dialog-model') + '/' + $F('link-dialog-inst');
			var selected = $('link-dialog-inst').childElements().find(function (x) {return x.selected;});
			LinkDialog.insert(link, selected.firstChild.nodeValue);
		}
		else {
			LinkDialog.insert($F('link-dialog-abslink'));
		}

		LinkDialog.close();
	},

	insert: function (link, name) {
		var selection = LinkDialog.textarea.getSelection();  
		LinkDialog.textarea.replaceSelection('[' + (selection == '' ? ((name) ? name : link) : selection) + '](' + link.replace(/^(?!(ftp|https?|internal):)/, 'http://') + ')');  
	},

	close: function () {
		LinkDialog.modelwatcher.stop();
		$('link-dialog').remove();
	},

	updateModels: function(options) {
		for (i in options) {
			$('link-dialog-model').appendChild(new Element('option', {value: i}).update(options[i]));
		}
	},

	updateInstances: function(options) {
		$('link-dialog-inst').update('');
		for (i in options) {
			$('link-dialog-inst').appendChild(new Element('option', {value: i}).update(options[i]));
		}
	},

	refreshInstances: function(el, value) {
		new Ajax.Request('/admin/markdown/links?model=' + value, {method: 'GET'})
	},
};
