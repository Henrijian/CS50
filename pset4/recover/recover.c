#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>

// JPEGs-related data types
typedef uint8_t  BYTE;
typedef uint8_t FAT_BLOCK [512];

bool is_start_block_of_jpeg(FAT_BLOCK block);
void store_jpeg_to_file(FAT_BLOCK jpeg[], int jpeg_size, char *file_name);

int main(int argc, char *argv[])
{
    // Ensure only one command-line argument
    if (argc != 2)
    {
        fprintf(stderr, "Usage: ./recover image\n");
        return 1;
    }
    // Ensure the specified file assigned by argument can be opened
    char *in_file_name = argv[1];
    FILE *in_file = fopen(in_file_name, "r");
    if (in_file == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", in_file_name);
        return 1;
    }


    int jpeg_buffer_size = 0;
    int jpeg_buffer_count = 0;
    long buffer_start_position = -1;
    // Iterate the blocks in file til the end
    const int each_read_num = 1;
    bool end_of_file = false;
    while (! end_of_file)
    {
        FAT_BLOCK block;
        int read_num = fread(&block, sizeof(FAT_BLOCK), each_read_num, in_file);
        // If a block can be read
        if (read_num == each_read_num)
        {
            if (buffer_start_position != -1)
            {
                // If the block is in starting format of jpeg, store the existing jpeg buffer into a file then
                // initialize the jpeg buffer with the block just read
                if (is_start_block_of_jpeg(block))
                {
                    long cur_position = ftell(in_file);

                    // Load into jpeg buffer
                    fseek(in_file, buffer_start_position, SEEK_SET);
                    FAT_BLOCK *jpeg_buffer = calloc(jpeg_buffer_size, sizeof(FAT_BLOCK));
                    fread(jpeg_buffer, sizeof(FAT_BLOCK), jpeg_buffer_size, in_file);
                    // Create file name, format:"XXX.jpg"
                    char file_name[8];
                    sprintf(file_name, "%03d.jpg", jpeg_buffer_count);
                    jpeg_buffer_count += 1;
                    // Write jpeg buffer into file
                    store_jpeg_to_file(jpeg_buffer, jpeg_buffer_size, file_name);
                    // Free loaded jpeg buffer
                    free(jpeg_buffer);

                    fseek(in_file, cur_position, SEEK_SET);
                    jpeg_buffer_size = 1;
                    buffer_start_position = ftell(in_file) - sizeof(FAT_BLOCK);
                }
                else
                {
                    // If the block is not in starting format of jpeg, update size of buffer
                    jpeg_buffer_size += 1;
                }
            }
            else
            {
                // If the block is in starting format of jpeg, Initialize the jpeg buffer with block and size
                if (is_start_block_of_jpeg(block))
                {
                    jpeg_buffer_size = 1;
                    buffer_start_position = ftell(in_file) - sizeof(FAT_BLOCK);
                }
            }
        }
        else
        {
            end_of_file = true;
        }
    }

    // If there is an existing jpeg buffer, find the last block of the jpeg buffer, then store this buffer into a file
    if (buffer_start_position != -1)
    {
        fseek(in_file, buffer_start_position, SEEK_SET);
        FAT_BLOCK *jpeg_buffer = calloc(jpeg_buffer_size, sizeof(FAT_BLOCK));
        fread(jpeg_buffer, sizeof(FAT_BLOCK), jpeg_buffer_size, in_file);
        char file_name[8];
        sprintf(file_name, "%03d.jpg", jpeg_buffer_count);
        store_jpeg_to_file(jpeg_buffer, jpeg_buffer_size, file_name);
        free(jpeg_buffer);
    }

    fclose(in_file);
    return 0;
}

bool is_start_block_of_jpeg(FAT_BLOCK block)
{
    BYTE first_byte = block[0];
    BYTE second_byte = block[1];
    BYTE third_byte = block[2];
    BYTE fourth_byte = block[3];
    if (first_byte == 0xff && second_byte == 0xd8 && third_byte == 0xff && 0xe0 <= fourth_byte && fourth_byte <= 0xef)
    {
        return true;
    }
    else
    {
        return false;
    }
}

void store_jpeg_to_file(FAT_BLOCK jpeg[], int jpeg_size, char *file_name)
{
    FILE *out_file = fopen(file_name, "w");
    if (out_file != NULL)
    {
        for (int i = 0; i < jpeg_size; i++)
        {
            fwrite(jpeg[i], sizeof(FAT_BLOCK), 1, out_file);
        }
        fclose(out_file);
    }
    return;
}