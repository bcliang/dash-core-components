if (!window.dash_clientside) {
    window.dash_clientside = {};
}

if (!window.GRAPH_DIV_ID) {
    window.GRAPH_DIV_ID = "clientside-graph";
}

window.dash_clientside.pytest = {
    relayout: function(button_click, fig) {
        // update only values within nested objects
        const update = {
            "title.text": fig.layout.title + "-new"
        };
        console.log('update,', update);
        Plotly.relayout(window.GRAPH_DIV_ID, update);

        return true;
    },


};
