#include "helpers.h"
#include <math.h>
#include <stdlib.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int y = 0; y < height; y++)
    {
        for (int x = 0; x < width; x++)
        {
            RGBTRIPLE *pixel = &image[y][x];
            BYTE gray_degree = round((float)((*pixel).rgbtBlue + (*pixel).rgbtGreen + (*pixel).rgbtRed) / 3);
            (*pixel).rgbtBlue = gray_degree;
            (*pixel).rgbtGreen = gray_degree;
            (*pixel).rgbtRed = gray_degree;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int y = 0; y < height; y++)
    {
        for (int x = 0, mid = floor(width / 2); x < mid; x++)
        {
            RGBTRIPLE *left_pixel = &image[y][x];
            RGBTRIPLE *right_pixel = &image[y][width - 1 - x];
            RGBTRIPLE temp_pixel = *left_pixel;
            *left_pixel = *right_pixel;
            *right_pixel = temp_pixel;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE(*temp_image)[width] = calloc(height, width * sizeof(RGBTRIPLE));
    for (int y = 0; y < height; y++)
    {
        for (int x = 0; x < width; x++)
        {
            int blur_red = 0;
            int blur_green = 0;
            int blur_blue = 0;
            int counter = 0;
            for (int i = y - 1; i <= y + 1; i ++)
            {
                for (int j = x - 1; j <= x + 1; j++)
                {
                    if (0 <= i && i < height && 0 <= j && j < width)
                    {
                        RGBTRIPLE round_pixel = image[i][j];
                        blur_red += round_pixel.rgbtRed;
                        blur_green += round_pixel.rgbtGreen;
                        blur_blue += round_pixel.rgbtBlue;
                        counter++;
                    }
                }
            }
            blur_red = round((float)blur_red / (float)counter);
            blur_green = round((float)blur_green / (float)counter);
            blur_blue = round((float)blur_blue / (float)counter);
            RGBTRIPLE *temp_pixel = &temp_image[y][x];
            (*temp_pixel).rgbtBlue = blur_blue;
            (*temp_pixel).rgbtGreen = blur_green;
            (*temp_pixel).rgbtRed = blur_red;
        }
    }
    for (int y = 0; y < height; y++)
    {
        for (int x = 0; x < width; x++)
        {
            image[y][x] = temp_image[y][x];
        }
    }
    free(temp_image);
    return;
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    const BYTE max_color_degree = 255;
    RGBTRIPLE(*temp_image)[width] = calloc(height, width * sizeof(RGBTRIPLE));
    for (int y = 0; y < height; y++)
    {
        for (int x = 0; x < width; x++)
        {
            int gx_red = 0;
            int gx_green = 0;
            int gx_blue = 0;
            for (int i = x - 1; i <= x + 1; i++)
            {
                if (0 <= i && i < width && i != x)
                {
                    for (int j = y - 1; j <= y + 1; j++)
                    {
                        if (0 <= j && j < height)
                        {
                            int multiplier;
                            if (j == y)
                            {
                                multiplier = 2;
                            }
                            else
                            {
                                multiplier = 1;
                            }
                            if (i == x - 1)
                            {
                                multiplier *= -1;
                            }
                            gx_red += image[j][i].rgbtRed * multiplier;
                            gx_green += image[j][i].rgbtGreen * multiplier;
                            gx_blue += image[j][i].rgbtBlue * multiplier;
                        }
                    }
                }
            }

            int gy_red = 0;
            int gy_green = 0;
            int gy_blue = 0;
            for (int i = y - 1; i <= y + 1; i++)
            {
                if (0 <= i && i < height && i != y)
                {
                    for (int j = x - 1; j <= x + 1; j++)
                    {
                        if (0 <= j && j < width)
                        {
                            int multiplier;
                            if (j == x)
                            {
                                multiplier = 2;
                            }
                            else
                            {
                                multiplier = 1;
                            }
                            if (i == y - 1)
                            {
                                multiplier *= -1;
                            }
                            gy_red += image[i][j].rgbtRed * multiplier;
                            gy_green += image[i][j].rgbtGreen * multiplier;
                            gy_blue += image[i][j].rgbtBlue * multiplier;
                        }
                    }
                }
            }

            unsigned int edge_red = round(sqrt(gx_red * gx_red + gy_red * gy_red));
            if (edge_red > max_color_degree)
                edge_red = max_color_degree;
            unsigned int edge_green = round(sqrt(gx_green * gx_green + gy_green * gy_green));
            if (edge_green > max_color_degree)
                edge_green = max_color_degree;
            unsigned int edge_blue = round(sqrt(gx_blue * gx_blue + gy_blue * gy_blue));
            if (edge_blue > max_color_degree)
                edge_blue = max_color_degree;

            RGBTRIPLE *temp_pixel = &temp_image[y][x];
            (*temp_pixel).rgbtRed = edge_red;
            (*temp_pixel).rgbtGreen = edge_green;
            (*temp_pixel).rgbtBlue = edge_blue;
        }
    }
    for (int y = 0; y < height; y++)
    {
        for (int x = 0; x < width; x++)
        {
            image[y][x] = temp_image[y][x];
        }
    }
    free(temp_image);
    return;
}
