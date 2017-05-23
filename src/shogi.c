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

static PyMethodDef shogi_methods[] = {
    {"error_out", (PyCFunction)error_out, METH_NOARGS, NULL},
    {"sum_test", (PyCFunction)sum_test, METH_VARARGS, NULL},
    {NULL, NULL}
};

#if PY_MAJOR_VERSION >= 3

static int shogi_traverse(PyObject *m, visitproc visit, void *arg) {
    Py_VISIT(GETSTATE(m)->error);
    return 0;
}

static int shogi_clear(PyObject *m) {
    Py_CLEAR(GETSTATE(m)->error);
    return 0;
}


static struct PyModuleDef moduledef = {
    PyModuleDef_HEAD_INIT,
    "shogi",
    NULL,
    sizeof(struct module_state),
    shogi_methods,
    NULL,
    shogi_traverse,
    shogi_clear,
    NULL
};

#define INITERROR return NULL

PyMODINIT_FUNC
PyInit_shogi(void)

#else
#define INITERROR return

void
initshogi(void)
#endif
{
#if PY_MAJOR_VERSION >= 3
    PyObject *module = PyModule_Create(&moduledef);
#else
    PyObject *module = Py_InitModule("shogi", shogi_methods);
#endif

    if (module == NULL)
        INITERROR;
    struct module_state *st = GETSTATE(module);

    st->error = PyErr_NewException("shogi.Error", NULL, NULL);
    if (st->error == NULL) {
        Py_DECREF(module);
        INITERROR;
    }

    PyObject *shogi_dict = PyModule_GetDict(module);
    PyObject *shogi_sub_modules = PyList_New(0);
    PyList_Append(shogi_sub_modules, PyString_FromString("Move"));
    PyImport_ImportModuleEx("Board", shogi_dict, shogi_dict, "shogi");

//    PyModule_AddIntConstant(module, "__version__", SHOGI_MODULE_VERSION);
//    PyModule_AddStringConstant(module, "__version__", SHOGI_MODULE_VERSION);
#if PY_MAJOR_VERSION >= 3
    return module;
#endif
}
