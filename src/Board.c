#include "Python.h"

struct module_state {
    PyObject *error;
};

#if PY_MAJOR_VERSION >= 3
#define GETSTATE(m) ((struct module_state*)PyModule_GetState(m))
#else
#define GETSTATE(m) (&_state)
static struct module_state _state;
#endif

static PyObject *
error_out(PyObject *m) {
    struct module_state *st = GETSTATE(m);
    PyErr_SetString(st->error, "something bad happened");
    return NULL;
}

static PyObject *
sum_test(PyObject *self, PyObject *args) {
    return Py_BuildValue("i", 42);
}

static PyMethodDef Board_methods[] = {
    {"error_out", (PyCFunction)error_out, METH_NOARGS, NULL},
    {"sum_test", (PyCFunction)sum_test, METH_VARARGS, NULL},
    {NULL, NULL}
};

#if PY_MAJOR_VERSION >= 3

static int Board_traverse(PyObject *m, visitproc visit, void *arg) {
    Py_VISIT(GETSTATE(m)->error);
    return 0;
}

static int Board_clear(PyObject *m) {
    Py_CLEAR(GETSTATE(m)->error);
    return 0;
}


static struct PyModuleDef moduledef = {
    PyModuleDef_HEAD_INIT,
    "Board",
    NULL,
    sizeof(struct module_state),
    Board_methods,
    NULL,
    Board_traverse,
    Board_clear,
    NULL
};

#define INITERROR return NULL

PyMODINIT_FUNC
PyInit_Board(void)

#else
#define INITERROR return

void
initBoard(void)
#endif
{
#if PY_MAJOR_VERSION >= 3
    PyObject *module = PyModule_Create(&moduledef);
#else
    PyObject *module = Py_InitModule("Board", Board_methods);
#endif

    if (module == NULL)
        INITERROR;
    struct module_state *st = GETSTATE(module);

    st->error = PyErr_NewException("Board.Error", NULL, NULL);
    if (st->error == NULL) {
        Py_DECREF(module);
        INITERROR;
    }

#if PY_MAJOR_VERSION >= 3
    return module;
#endif
}
