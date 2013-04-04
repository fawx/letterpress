app.LetterView = Backbone.View.extend({
    events: {
        'click': 'toggle',
    },


    template: _.template( $('#letter-template').html() ),


    initialize: function() {
        this.listenTo(this.model, 'change', this.render);
    },


    render: function() {
        var inPlay = this.model.get('inPlay'),
            locked = this.model.get('locked'),
            owner = this.model.get('owner');

        this.$el.toggleClass('in-play', inPlay !== false);
        this.$el.toggleClass('locked', locked);

        if (owner) {
            this.$el.addClass(( owner == app.view.get_current_player() ? 'mine' : 'theirs' ))
        }

        this.$el.html( this.template( this.model.toJSON() ) );
        
        return this;
    },


    toggle: function() {
        if ( this.game.my_turn() ) {
            this.model.toggle();
        }
    }
});
