app.GameView = Backbone.View.extend({
    className: 'game',



    template: _.template( $('#game-template').html() ),



    events: {
        'click .save': 'submit_word',
    },



    subviews: {
        letters: undefined,
        in_play: undefined
    },


    initialize: function() {
        this.subviews.in_play = new app.PlayView({ 
            tagName: 'ul', 
            collection: new app.Play() 
        });

        this.subviews.in_play.listenTo(this.model.get('letters'), 'change:inPlay', this.subviews.in_play.update);
    },



    render: function() {
        var $letters = $('<ul>'),
            thisview = this;


        // create the template
        this.$el.html('').append( this.template( this.model.toJSON() ) );


        // create the letters
        this.model.get('letters').each(function(letter) {
            var view = new app.LetterView({ 
                tagName: 'li',
                model: letter
            });

            view.game = thisview;

            $letters.append(view.render().el);
        });


        // insert the letters
        this.$el.children('.board').html($letters);

        // letters in play
        this.$el.children('.play').children('.letters').html(this.subviews.in_play.render().el);


        return this;
    },



    submit_word: function() {
        var thisview = this;

        // TODO: 
        // only send letters that have changed inPlay
        this.model.save(this.model.attributes, {
            success: function(model, response, options) {
                thisview.subviews.in_play.collection.reset();
                thisview.subviews.in_play.render();
                thisview.render();
            },
            error: function(model, xhr, options) {
                console.log(xhr.responseText);
            },
            wait: true,
        });
    },



    my_turn: function() {
        return this.model.get('turn') == app.view.get_current_player();
    }
})