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

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    const BYTE max_color_degree = 255;
    for (int y = 0; y < height; y++)
    {
        for (int x = 0; x < width; x++)
        {
            RGBTRIPLE *pixel = &image[y][x];
            int sepia_red = round(0.393 * (*pixel).rgbtRed + 0.769 * (*pixel).rgbtGreen + 0.189 * (*pixel).rgbtBlue);
            if (sepia_red > max_color_degree)
                sepia_red = max_color_degree;
            int sepia_green = round(0.349 * (*pixel).rgbtRed + 0.686 * (*pixel).rgbtGreen + 0.168 * (*pixel).rgbtBlue);
            if (sepia_green > max_color_degree)
                sepia_green = max_color_degree;
            int sepia_blue = round(0.272 * (*pixel).rgbtRed + 0.534 * (*pixel).rgbtGreen + 0.131 * (*pixel).rgbtBlue);
            if (sepia_blue > max_color_degree)
                sepia_blue = max_color_degree;
            (*pixel).rgbtBlue = sepia_blue;
            (*pixel).rgbtGreen = sepia_green;
            (*pixel).rgbtRed = sepia_red;
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
            RGBTRIPLE *pixl = &image[y][x];
            RGBTRIPLE *temp_pixel = &temp_image[y][x];
            *pixl = *temp_pixel;
        }
    }
    free(temp_image);
    return;
}
