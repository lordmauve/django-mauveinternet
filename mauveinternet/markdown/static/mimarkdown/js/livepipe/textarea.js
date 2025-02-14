/**
 * @author Ryan Johnson <http://saucytiger.com/>
 * @copyright 2008 PersonalGrid Corporation <http://personalgrid.com/>
 * @package LivePipe UI
 * @license MIT
 * @url http://livepipe.net/control/textarea
 * @require prototype.js, livepipe.js
 */

if(typeof(Prototype) == "undefined")
	throw "Control.TextArea requires Prototype to be loaded.";
if(typeof(Object.Event) == "undefined")
	throw "Control.TextArea requires Object.Event to be loaded.";

Control.TextArea = Class.create({
	initialize: function(textarea){
		this.onChangeTimeout = false;
		this.element = $(textarea);
		$(this.element).observe('keyup',this.doOnChange.bindAsEventListener(this));
		$(this.element).observe('paste',this.doOnChange.bindAsEventListener(this));
		$(this.element).observe('input',this.doOnChange.bindAsEventListener(this));
		if(!!document.selection){
			$(this.element).observe('mouseup',this.saveRange.bindAsEventListener(this));  
			$(this.element).observe('keyup',this.saveRange.bindAsEventListener(this));
		}
	},
	doOnChange: function(event){
		if(this.onChangeTimeout)
			window.clearTimeout(this.onChangeTimeout);
		this.onChangeTimeout = window.setTimeout(function(){
			this.notify('change',this.getValue());
		}.bind(this),Control.TextArea.onChangeTimeoutLength);
	},
	saveRange: function(){
		this.range = document.selection.createRange();  
	},
	getValue: function(){
		return this.element.value;
	},
	getSelection: function(){
		if(!!document.selection)
			return document.selection.createRange().text;
		else if(!!this.element.setSelectionRange)
			return this.element.value.substring(this.element.selectionStart,this.element.selectionEnd);
		else
			return false;
	},
	getSelectionStart: function() {
		if(!!this.element.setSelectionRange)
			return this.element.selectionStart;
		else if(!!document.selection)
		{
			// The current selection
			var range = document.selection.createRange();
			// We'll use this as a 'dummy'
			var stored_range = range.duplicate();
			// Select all text
			stored_range.moveToElementText( this.element );
			// Now move 'dummy' end point to end point of original range
			stored_range.setEndPoint( 'EndToEnd', range );
			// Now we can calculate start and end points
			return stored_range.text.length - range.text.length;
			//element.selectionEnd = element.selectionStart + range.text.length;
		}
		else
			return 0;
	},
	replaceSelection: function(text){
		var scroll_top = this.element.scrollTop;
		if(!!document.selection){
			this.element.focus();
			var range = (this.range) ? this.range : document.selection.createRange();
			range.text = text;
			range.select();
		}else if(!!this.element.setSelectionRange){
			var selection_start = this.element.selectionStart;
			this.element.value = this.element.value.substring(0,selection_start) + text + this.element.value.substring(this.element.selectionEnd);
			this.element.setSelectionRange(selection_start + text.length,selection_start + text.length);
		}
		this.doOnChange();
		this.element.focus();
		this.element.scrollTop = scroll_top;
	},
	wrapSelection: function(before,after){
		this.replaceSelection(before + this.getSelection() + after);
	},
	insertBeforeSelection: function(text){
		this.replaceSelection(text + this.getSelection());
	},
	insertAfterSelection: function(text){
		this.replaceSelection(this.getSelection() + text);
	},
	collectFromEachSelectedLine: function(callback,before,after){
		this.replaceSelection((before || '') + $A(this.getSelection().split("\n")).collect(callback).join("\n") + (after || ''));
	},
	insertBeforeEachSelectedLine: function(text,before,after){
		this.collectFromEachSelectedLine(function(line){
		},before,after);
	}
});
Object.extend(Control.TextArea,{
	onChangeTimeoutLength: 500
});
Object.Event.extend(Control.TextArea);

Control.TextArea.ToolBar = Class.create(	{
	initialize: function(textarea,toolbar){
		this.textarea = textarea;
		if(toolbar)
			this.container = $(toolbar);
		else{
			this.container = $(document.createElement('ul'));
			this.textarea.element.parentNode.insertBefore(this.container,this.textarea.element);
		}
	},
	attachButton: function(node,callback){
		node.onclick = function(){return false;}
		$(node).observe('click',callback.bindAsEventListener(this.textarea));
	},
	addButton: function(link_text,callback,attrs){
		var li = document.createElement('li');
		var a = document.createElement('a');
		a.href = '#';
		this.attachButton(a,callback);
		li.appendChild(a);
		Object.extend(a,attrs || {});
		if(link_text){
			var span = document.createElement('span');
			span.innerHTML = link_text;
			a.appendChild(span);
		}
		this.container.appendChild(li);
	}
});
