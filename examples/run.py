from examples import intro, callback, figure_n_slider, \
    multiple_inputs, multiple_outputs, chained_callback, \
    table_callback, state_callback, print_graph, hover_update_graph, \
    cross_filter, prevent_update, no_update, callback_context, \
    first_load, indirect_result, prevent_initial_call, sync_slider_text, \
    convert_temperature, sync_checklists, clientside_callbacks, \
    clientside_callbacks_px, all_pattern, match_pattern, allsmaller_pattern, \
    todo, store_clicks, reusable_components, external_resources, live_update, \
    share_data_callbacks, simple_slider, \
    simple_range_slider, mark_range_slider

import dash
dash.register_page(__name__)
def callback_example(pathname):
    if pathname == '/examples/intro':
        return intro.layout
    elif pathname == '/examples/callback':
        return callback.layout
    elif pathname == '/examples/figure-n-slider':
        return figure_n_slider.layout
    elif pathname == '/examples/multiple-inputs':
        return multiple_inputs.layout
    elif pathname == '/examples/multiple-outputs':
        return multiple_outputs.layout
    elif pathname == '/examples/chained-callback':
        return chained_callback.layout
    elif pathname == '/examples/table-callback':
        return table_callback.layout
    elif pathname == '/examples/state-callback':
        return state_callback.layout
    elif pathname == '/examples/print-graph':
        return print_graph.layout
    elif pathname == '/examples/hover-update-graph':
        return hover_update_graph.layout
    elif pathname == '/examples/cross-filter':
        return cross_filter.layout
    elif pathname == '/examples/prevent-update':
        return prevent_update.layout
    elif pathname == '/examples/no-update':
        return no_update.layout
    elif pathname == '/examples/callback-context':
        return callback_context.layout
    elif pathname == '/examples/first-load':
        return first_load.layout
    elif pathname == '/examples/indirect-result':
        return indirect_result.layout
    elif pathname == '/examples/prevent-initial-call':
        return prevent_initial_call.layout
    elif pathname == '/examples/sync-slider-text':
        return sync_slider_text.layout
    elif pathname == '/examples/convert-temperature':
        return convert_temperature.layout
    elif pathname == '/examples/sync-checklists':
        return sync_checklists.layout
    elif pathname == '/examples/clientside-callbacks':
        return clientside_callbacks.layout
    elif pathname == '/examples/clientside-callbacks-px':
        return clientside_callbacks_px.layout
    elif pathname == '/examples/all-pattern':
        return all_pattern.layout
    elif pathname == '/examples/match-pattern':
        return match_pattern.layout
    elif pathname == '/examples/allsmaller-pattern':
        return allsmaller_pattern.layout
    elif pathname == '/examples/todo':
        return todo.layout
    elif pathname == '/examples/store-clicks':
        return store_clicks.layout
    elif pathname == '/examples/reusable-components':
        return reusable_components.layout
    elif pathname == '/examples/external-resources':
        return external_resources.layout
    elif pathname == '/examples/live-update':
        return live_update.layout
    # elif pathname == '/examples/flask-caching':
    #     return flask_caching.layout
    # elif pathname == '/examples/caching-dataset':
    #     return caching_dataset.layout
    elif pathname == '/examples/share-data-callbacks':
        return share_data_callbacks.layout
    elif pathname == '/examples/simple-slider':
        return simple_slider.layout
    elif pathname == '/examples/simple-range-slider':
        return simple_range_slider.layout
    elif pathname == '/examples/mark-range-slider':
        return mark_range_slider.layout
    else:
        return "No layout"
