=======
Caveats
=======

Views are not cached, but boxes (some of them) maintain references in themselves.
Maybe it comes from Python and byte code, when an instance / object is created
without dynamic arguments, but it seems that if we use persistence, memory can be
filled really quick. Not using persistence, computations are done several time
(waste, see logs list in meerkat). All of this could be solved by improving the way
boxes compute stuff: using database retrievals instead of parsing files (see meerkat
logs) each time.

- Persistent argument allows you to call a callable attribute of a box several times
  in a template without recomputing the data each time. It is run once then first result
  is always used.

- Lazy argument allows you to have the callable called only when entering the template
  rendering. If not lazy, callable is called immediately when the box is created.
  Lazy is only useful with persistent=True.

- There is a difference if the box is instantiated as class variable (1) or in a custom
  get method (2):

  1) persistent for the worker's life-time, lazy at startup (first request) -> rendering
  2) persistent for the rendering function period, lazy at view call (box creation) -> rendering

- WARNING: in both cases, persistence can lead to memory consumption, freed either when GC
  is called or worker is relaunched.
