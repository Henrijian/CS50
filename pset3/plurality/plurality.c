#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <limits.h>
#include <math.h>

// Max number of candidates
#define MAX 9

// Candidates have name and vote count
typedef struct
{
    string name;
    int votes;
}
candidate;

// Array of candidates
candidate candidates[MAX];

// Number of candidates
int candidate_count;

// Function prototypes
bool vote(string name);
void print_winner(void);

int main(int argc, string argv[])
{
    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: plurality [candidate ...]\n");
        return 1;
    }

    // Populate array of candidates
    candidate_count = argc - 1;
    if (candidate_count > MAX)
    {
        printf("Maximum number of candidates is %i\n", MAX);
        return 2;
    }
    for (int i = 0; i < candidate_count; i++)
    {
        candidates[i].name = argv[i + 1];
        candidates[i].votes = 0;
    }

    int voter_count = get_int("Number of voters: ");

    // Loop over all voters
    for (int i = 0; i < voter_count; i++)
    {
        string name = get_string("Vote: ");

        // Check for invalid vote
        if (!vote(name))
        {
            printf("Invalid vote.\n");
        }
    }

    // Display winner of election
    print_winner();
}

void bubble_sort(candidate candidate_list[], int count)
{
    bool no_sort_happen;
    for (int i = 0; i < count - 1; i++)
    {
        no_sort_happen = true;
        for (int j = 0; j < count - 1 - i; j++)
        {
            if (candidate_list[j].votes > candidate_list[j + 1].votes)
            {
                candidate tmp_candidate = candidate_list[j];
                candidate_list[j] = candidate_list[j + 1];
                candidate_list[j + 1] = tmp_candidate;
                no_sort_happen = false;
            }
        }
        if (no_sort_happen)
        {
            break;
        }
    }
}

void merge_sort(candidate candidate_list[], int start, int end)
{
    if (start == end)
    {
        return;
    }
    else
    {
        int mid = round((start + end) / 2);

        // merge sort left side
        int left_count = mid - start + 1;
        candidate left_candidates[left_count];
        int left_i = 0;
        for (int i = start; i <= mid; i++)
        {
            left_candidates[left_i].name = candidate_list[i].name;
            left_candidates[left_i].votes = candidate_list[i].votes;
            left_i++;
        }
        merge_sort(left_candidates, 0, left_count - 1);

        // merge sort right side
        int right_count = end - mid;
        candidate right_candidates[right_count];
        int right_i = 0;
        for (int i = mid + 1; i <= end; i++)
        {
            right_candidates[right_i].name = candidate_list[i].name;
            right_candidates[right_i].votes = candidate_list[i].votes;
            right_i++;
        }
        merge_sort(right_candidates, 0, right_count - 1);

        // merge left and right side
        left_i = 0;
        right_i = 0;
        for (int i = start; i <= end; i++)
        {
            int right_votes = INT_MAX;
            if (right_i < right_count)
            {
                right_votes = right_candidates[right_i].votes;
            }

            int left_votes = INT_MAX;
            if (left_i < left_count)
            {
                left_votes = left_candidates[left_i].votes;
            }

            if (right_votes < left_votes)
            {
                candidate_list[i].name = right_candidates[right_i].name;
                candidate_list[i].votes = right_candidates[right_i].votes;
                right_i++;
            }
            else
            {
                candidate_list[i].name = left_candidates[left_i].name;
                candidate_list[i].votes = left_candidates[left_i].votes;
                left_i++;
            }
        }

    }
}

// Update vote totals given a new vote
bool vote(string name)
{
    for (int i = 0; i < candidate_count; i++)
    {
        if (strcmp(name, candidates[i].name) == 0)
        {
            candidates[i].votes += 1;
            return true;
        }
    }
    return false;
}

// Print the winner (or winners) of the election
void print_winner(void)
{
    //bubble_sort(candidates, candidate_count);
    merge_sort(candidates, 0, candidate_count-1);
    int highest_votes = candidates[candidate_count - 1].votes;
    for (int i = candidate_count - 1; 0 <= i; i--)
    {
        if (candidates[i].votes == highest_votes)
        {
            printf("%s\n", candidates[i].name);
        }
        else
        {
            break;
        }
    }
    return;
}

