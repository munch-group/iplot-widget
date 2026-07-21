
from .iplot import iplot, iplot_settings


# import sys
# import ipywidgets
# from IPython.display import display 
# import seaborn as sns
# import matplotlib.pyplot as plt

# _graphics = [
#     sns.boxplot, 
#     sns.scatterplot, 
#     sns.violinplot,
#     sns.boxenplot, 
#     sns.swarmplot,
#     sns.stripplot,
#     sns.kdeplot,
#     sns.barplot,
# ]

# def iplot(df, graphics=_graphics, 
#               strings_as_cats=False, palette="colorblind", style='darkgrid', figsize=(8,4), **kwargs):

#     def plot(selected_x, selected_y, selected_hue=None, selected_plot=graphics[0]):
#         plt.close('all')
#         fig, ax = plt.subplots(1, 1, figsize=figsize)
#         sns.set_style(style)
#         sns.set_palette(palette)
#         kwargs = dict(x=df[selected_x], y=df[selected_y])
#         if selected_hue in df:
#             kwargs['hue'] = df[selected_hue]
#             # kwargs['palette'] = palette
#         try:
#             selected_plot(**kwargs, ax=ax)
#         except TypeError as e:
#             print(f"{str(e).split(',')[0]}. That does not compatible with {selected_plot.__name__}", file=sys.stderr)
#             plt.close('all')            
#             return
#         plt.title(f'{selected_plot.__name__.capitalize()} of {selected_y} against {selected_x}')
#         handles, labels = ax.get_legend_handles_labels()
#         if labels:
#             ax.legend(loc='center left', framealpha=0, bbox_to_anchor=(1, 0.5))
#         # sns.despine()
#         plt.show()
    
#     categorical_col_names = df.columns[(df.map(type) == str).all(0)].to_list()

#     dropdowns = {}
#     if 'plot' in kwargs:
#         plot_options = [(g.__name__, g) for g in graphics]
#         names, funs = zip(*plot_options)
#         i = names.index(kwargs['plot'])
#         options = plot_options[i:i+1] + plot_options[:i] + plot_options[i+1:] 
#         drop_down_plot = ipywidgets.Dropdown(options=options, description='Plot:', disabled=False)
#         dropdowns['selected_plot'] = drop_down_plot
#     if 'x' in kwargs:
#         x_options = df.columns.to_list()
#         drop_down_x = ipywidgets.Dropdown(options=x_options, value=kwargs['x'], description='X variable:', disabled=False)
#         dropdowns['selected_x'] = drop_down_x
#     if 'y' in kwargs:
#         if strings_as_cats:
#             y_options = df.drop(categorical_col_names,axis=1).columns
#         else:
#             y_options = df.columns.to_list()
#         drop_down_y = ipywidgets.Dropdown(options=y_options, value=kwargs['y'], description='Y variable:', disabled=False)
#         dropdowns['selected_y'] = drop_down_y
#     if 'hue' in kwargs:
#         if strings_as_cats:
#             hue_options = df.columns[(df.map(type) == str).all(0)]
#         else:
#             hue_options = df.columns.to_list()
#         drop_down_hue= ipywidgets.Dropdown(options=hue_options, value=kwargs['hue'], description='Hue:', disabled=False)
#         dropdowns['selected_hue'] = drop_down_hue

#     display(ipywidgets.HBox(list(dropdowns.values())),
#             ipywidgets.interactive_output(plot, dropdowns))
