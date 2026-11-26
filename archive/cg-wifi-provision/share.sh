echo "=== DIRECTORY STRUCTURE ==="; \
find main  -maxdepth 2 -not -path '*/.*'; \
echo "\n=== FILE CONTENTS ==="; \
find main . -maxdepth 2 -type f \
\( -name "*.cpp" -o -name "*.h" -o -name "*.c" -o -name "*.html" -o -name "*.css" -o -name "*.js" -o -name "*.ini" -o -name "partitions.csv" -o -name "CMakeLists.txt" \) \
-not -path '*/.pio/*' \
-exec sh -c 'echo "\n\n----------------------------------------------------------------------"; echo ">>> FILE: {}"; echo "----------------------------------------------------------------------"; cat "{}"' \;
