#include <iostream>
#include <vector>
#include <stdexcept>

int main()
{
    std::vector<int> sampleVector;

    // sampleVectorのindex0～9に要素を詰める. 
    for (int i = 0; i < 10; i++)
    {
        sampleVector.push_back(i);
    }

    std::cout << "###std::vector::at" << std::endl;

    // at
    try
    {
        // sampleVectorの管理範囲外であるindex10の要素にアクセスする. 
        for (int i = 1; i <= 10; i++)
        {
            std::cout << sampleVector.at(i) << std::endl;
        }

        // atの境界チェックで例外を投げるため、この処理は実行されない. 
        std::cout << "Complete..." << std::endl;
    }
    catch (std::out_of_range& sampleException)
    {
        std::cout << "out of range!" << std::endl;
        std::cout << "Error : " << sampleException.what() << std::endl;
    }

    std::cout << std::endl << "###std::vector::operator[]" << std::endl;

    // operator[]
    try
    {
        // sampleVectorの管理範囲外であるindex10の要素にアクセスする. 
        for (int i = 1; i <= 10; i++)
        {
            std::cout << sampleVector[i] << std::endl;
        }

        // 境界チェック無しのため、そのまま不定値が出力され、実行完了となる. 
        std::cout << "Complete..." << std::endl;
    }
    // 境界チェック無しのため、例外は投げない. 
    catch (std::out_of_range& sampleException)
    {
        std::cout << "out of range!" << std::endl;
        std::cout << "Error : " << sampleException.what() << std::endl;
    }

    std::cout << "End..." << std::endl;

    return 0;
}