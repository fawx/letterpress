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
        this.eventhub = _.extend({}, Backbone.Events);

        this.eventhub.on('error', this.error);
        this.eventhub.on('message', this.message);

    },



    render: function() {
        var $letters = $('<ul>'),
            thisview = this;


        

        // this should be in initialize()
        // maybe?  where's the harm if it's created every time the board is rendered?
        //
        var play = new app.Play();

        this.subviews.in_play = new app.PlayView({ 
            tagName: 'ul', 
            collection: play
        });

        this.subviews.in_play.listenTo(this.model.get('letters'), 'change:inPlay', this.subviews.in_play.update);
        //
        ////////////////////////////////



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


        if ( this.my_turn() ) {
            var word = '';

            this.subviews.in_play.collection.each(function(letter) {
                word += letter.get('character');
            });

            // TODO: 
            // only send letters that have changed inPlay
            this.model.save(this.model.attributes, {
                success: function(model, response, options) {
                    thisview.render();

                    thisview.eventhub.trigger('message', 'You played <span>' + word + '</span>.');
                },
                error: function(model, xhr, options) {
                    thisview.eventhub.trigger('error', '<span>' + word + '</span> is not a valid word (either not in dictionary or has been played before)')
                },
                wait: true,
            });
        }
        else {
            thisview.eventhub.trigger('error', 'It\'s not your turn.');
        }
    },



    my_turn: function() {
        return this.model.get('turn') == app.view.get_current_player();
    },



    error: function(message) {
        console.log('error: ' + message);
    },



    message: function(message) {
        console.log('message: ' + message);
    },
});
