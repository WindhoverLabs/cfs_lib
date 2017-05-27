
add_airliner_app_def(cfs_lib
    FILE CFS_LIB
    SOURCES
        ${CMAKE_CURRENT_SOURCE_DIR}/../src/cfs_utils.c

    INCLUDES
        ${CMAKE_CURRENT_SOURCE_DIR}/../src/

    # This application has a public include header.  Add it so all the other applications can access it.
    PUBLIC_INCLUDES
        ${CMAKE_CURRENT_SOURCE_DIR}/../public_inc/
)
