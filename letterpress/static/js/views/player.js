app.PlayerView = Backbone.View.extend({
    template: _.template( $('#player-template').html() ),


    initialize: function() {
        var thisview = this;

        this.model.fetch({
            success: function(model, response, options) {
                thisview.render();
            }
        });
    },


    render: function() {
        this.$el.html( this.template( this.model.toJSON() ) );

        return this;
    },
});