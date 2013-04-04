app.Letter = Backbone.Model.extend({
    defaults: {
        character: '',
        owner: undefined,
        // TODO:
        // get rid of these attributes since they serve no purpose in the database
        inPlay: false,
        locked: false,
    },

    toggle: function() {
        // this is a real serious play on javascript's !n = false where n is a number
        this.set('inPlay', !this.get('inPlay'));
    }
});
