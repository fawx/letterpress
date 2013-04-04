app.PlayView = Backbone.View.extend({
    events: {
    },


    initialize: function() {
        this.listenTo(this.collection, 'add', this.render);
        this.listenTo(this.collection, 'remove', this.render);
    },


    render: function() {
        this.$el.html('');

        var i = 1;
        this.collection.each(function(letter) {
            letter.set('inPlay', i++);
            view = new app.LetterView({ 
                tagName: 'li',
                model: letter 
            });

            this.$el.append( view.render().el );
        }, this);

        return this;
    },


    update: function(letter) {
        if (letter.get('inPlay')) {
            this.collection.add(letter);
        }
        else {
            this.collection.remove(letter);
        }
    },
});
