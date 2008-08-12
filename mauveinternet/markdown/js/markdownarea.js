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

		//buttons  
		toolbar.addButton('Italics',function(){  
			this.wrapSelection('*','*');  
		},{  
			className: 'markdown_italics_button'  
		});  
		  
		toolbar.addButton('Bold',function(){  
			this.wrapSelection('**','**');  
		},{  
			className: 'markdown_bold_button'  
		});  
		  
		toolbar.addButton('Link',function(){  
			var selection = this.getSelection();  
			var response = prompt('Enter Link URL','');  
			if(response == null)  
				return;  
			this.replaceSelection('[' + (selection == '' ? 'Link Text' : selection) + '](' + (response == '' ? 'http://link_url/' : response).replace(/^(?!(f|ht)tps?:\/\/)/,'http://') + ')');  
		},{  
			className: 'markdown_link_button'  
		});  
		  
		toolbar.addButton('Image',function(){  
			var selection = this.getSelection();  
			var response = prompt('Enter Image URL','');  
			if(response == null)  
				return;  
			this.replaceSelection('![' + (selection == '' ? 'Image Alt Text' : selection) + '](' + (response == '' ? 'http://image_url/' : response).replace(/^(?!(f|ht)tps?:\/\/)/,'http://') + ')');  
		},{  
			className: 'markdown_image_button'  
		});  
		  
		toolbar.addButton('Heading',function(){  
			var selection = this.getSelection();  
			if(selection == '')  
				selection = 'Heading';  
			this.replaceSelection("\n" + selection + "\n" + $R(0,Math.max(5,selection.length)).collect(function(){'-'}).join('') + "\n");  
		},{  
			className: 'markdown_heading_button'  
		});  
		  
		toolbar.addButton('Unordered List',function(event){  
			this.collectFromEachSelectedLine(function(line){  
				return event.shiftKey ? (line.match(/^\*{2,}/) ? line.replace(/^\*/,'') : line.replace(/^\*\s/,'')) : (line.match(/\*+\s/) ? '*' : '* ') + line;  
			});  
		},{  
			className: 'markdown_unordered_list_button'  
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
			className: 'markdown_ordered_list_button'  
		});  
		  
		toolbar.addButton('Block Quote',function(event){  
			this.collectFromEachSelectedLine(function(line){  
				return event.shiftKey ? line.replace(/^\> /,'') : '> ' + line;  
			});  
		},{  
			className: 'markdown_quote_button'  
		});  
	});
});
