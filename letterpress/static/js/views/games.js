app.GamesView = Backbone.View.extend({
    subviews: {
        game: []
    },


    initialize: function() {
        var thisview = this;

        this.collection.fetch({
            success: function() {
                thisview.collection.each(function(game) {
                    thisview.subviews.game.push( new app.GameView({ model: game }) );
                });

                thisview.render();
            }
        });
    },


    render: function() {
        this.$el.html('');

        var thisview = this;
        
        _.each(this.subviews.game, function(gameview) {
            thisview.$el.append( gameview.render().el );
        });
        
        return this;
    },
});